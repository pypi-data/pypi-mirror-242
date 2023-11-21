import functools
import os
from typing import Tuple, List, Optional, Dict

import requests
import torch
from transformers import GenerationMixin, PreTrainedTokenizer
from supabase import create_client, Client
from postgrest.exceptions import APIError

# TODO: dotenv is a dev dependency, so this will fail in production
# from dotenv import load_dotenv, find_dotenv

_entity_name: Optional[str] = None
_project_name: Optional[str] = None
_task_name: Optional[str] = None
_run_name: Optional[str] = None
supabase: Client = None


def get_supabase_client():
    return supabase


def get_client_state() -> Tuple[str, str, str]:
    """Get (project_name, task_name, run_name)"""
    return _project_name, _task_name, _run_name


def init_required(func):
    """Make sure that init() has been called before calling the decorated function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _project_name or not _task_name or not _run_name or not supabase:
            raise Exception("goldenset not initialized. Please call gs.init()")
        return func(*args, **kwargs)

    return wrapper


# TODO: Make run_name optional
# TODO: See if team agrees that _name is redundant. run_name is left because wandb uses name
# TODO: We might want to move auth checks to here? Basically do the id resolves in init
def init(project: str, task: str, run_name: str, entity: Optional[str] = None):
    """Initialize run wth project_name, task_name, and run_name"""
    # TODO: dotenv is a dev dependency, so this will fail in production
    # load_dotenv(find_dotenv())

    global _entity_name
    global _project_name
    global _task_name
    global _run_name
    global supabase

    _entity_name = os.environ.get("GOLDENSET_ENTITY", entity)
    _project_name = os.environ.get("GOLDENSET_PROJECT", project)
    _task_name = os.environ.get("GOLDENSET_TASK", task)
    _run_name = os.environ.get("GOLDENSET_RUN_NAME", run_name)

    # TODO: Promote env var names to constants, and document them
    # TODO: Promote defaults to constants
    url: str = os.environ.get(
        "GOLDENSET_URL", "https://njsizbbehmmlwsvtkxyk.supabase.co"
    )
    key: str = os.environ.get(
        "GOLDENSET_ANON_KEY",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5qc2l6YmJlaG1tbHdzdnRreHlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk2NDAzODYsImV4cCI6MjAxNTIxNjM4Nn0.MT3585SXcYd4ivR41skp26Y0os1Rx5_AAt2ubapbNKQ",
    )
    supabase = create_client(url, key)

    api_key = os.environ.get("GOLDENSET_API_KEY", None)
    if api_key:
        # TODO: Not sure if the use of lambda here will cause pickle issues
        supabase._get_token_header = lambda: {"Authorization": api_key}
    else:
        raise Exception(
            "Not authenticated. Please set the GOLDENSET_API_KEY environment variable"
        )


def finish():
    """Finish the run"""
    global _entity_name
    global _project_name
    global _task_name
    global _run_name
    global supabase

    _entity_name = None
    _project_name = None
    _task_name = None
    _run_name = None
    supabase = None


def _resolve_ids() -> Tuple[str, str, str]:
    entity_id_response = (
        supabase.table("entity").select("id").eq("name", _entity_name).execute()
    )
    if not entity_id_response.data:
        raise ValueError(
            f"Entity {_entity_name} not found. Check that you have access to {_entity_name}"
        )

    entity_id = entity_id_response.data[0]["id"]

    # Get project_id and assert existence
    project_id_response = (
        supabase.table("project")
        .select("id")
        .eq("name", _project_name)
        .eq("entity_id", entity_id)
        .execute()
    )

    if not project_id_response.data:
        raise ValueError(f"Project {_entity_name}/{_project_name} not found")

    project_id = project_id_response.data[0]["id"]

    # Get task ID and assert existence
    task_id_response = (
        supabase.table("task")
        .select("id")
        .eq("project_id", project_id)
        .eq("name", _task_name)
        .execute()
    )
    if not task_id_response.data:
        raise ValueError(f"Task {_entity_name}/{_project_name}/{_task_name} not found")

    task_id = task_id_response.data[0]["id"]
    return entity_id, project_id, task_id


# TODO: We need to decide if its testset or goldenset
# TODO: Are we sure we want to return a list of dicts? This makes it difficult to batch inference
@init_required
def get_golden_set(version: Optional[int] = None) -> List[Dict[str, str]]:
    """
    Returns the golden set for the given project and task


    Parameters
    ----------
    version : Optional[int], optional
        The version of the goldenset to return, by default None

    Returns
    -------
    List[Dict[str, str]] : List of dictionaries containing the input and output of the golden set, as well as the test_set row id, necessary to log the outputs.
    """
    # Get entity_id and check that user can access
    _, _, task_id = _resolve_ids()

    # Obtain versioned testset id, otherwise take most recent
    if version is not None:
        testset_id_response = (
            supabase.table("testset")
            .select("id")
            .eq("task_id", task_id)
            .eq("version", version)
            .execute()
        )
        if not testset_id_response.data:
            raise ValueError(
                f"Version {version} not found for {_entity_name}/{_project_name}/{_task_name}"
            )
    else:
        testset_id_response = (
            supabase.table("testset")
            .select("id", "version")
            .eq("task_id", task_id)
            .order("version", desc=True)
            .execute()
        )

        if not testset_id_response.data:
            raise ValueError(f"Task {_task_name} has no saved testset")

        version = testset_id_response.data[0]["version"]

    testset_id = testset_id_response.data[0]["id"]

    # Get questions for a given testset_id  and assert existence
    testset_response = (
        supabase.table("testset_row")
        .select("id, input, output")
        .eq("testset_id", testset_id)
        .execute()
    )
    if not testset_response.data:
        raise ValueError(
            f"Testset {_entity_name}/{_project_name}/{_task_name}[v{version}] has no rows"
        )

    return [
        {"input": q["input"], "output": q["output"], "id": q["id"]}
        for q in testset_response.data
    ]


# TODO: Set a standard argument order for all functions E -> P -> T -> RS -> Run
# PK -> FK -> Data
def _create_run(run_name: str, task_id: str, entity_id: str) -> str | None:
    """
    Create a run in run table for a given task_id and entity_id

    Parameters
    ----------
    run_name : str
        Name of the run to be created
    task_id : str
        ID of the task the run belongs to, obtained from the task table by querying the task name
    entity_id : str
        ID of the entity creating the run

    Returns
    -------
    str | None : ID of the run created
    """
    # Create new run in run table and return ID
    run_insertion = (
        supabase.table("run")
        .insert(
            {
                "name": run_name,
                "task_id": task_id,
                "entity_id": entity_id,
            }
        )
        .execute()
    )
    if run_insertion.data:
        return run_insertion.data[0]["id"]

    raise Exception("Failed to create run")


def _populate_rows(
    entity_id: str, run_id: str, testset_row_ids: List[str], completions: List[str]
) -> List[Dict[str, str]]:
    """
    Function to populate the run_row table with the completions and testset_row_ids

    Parameters
    ----------
    entity_id : str
        ID of the entity creating the run
    run_id : str
        ID of the run the completions belong to
    completions : List[str]
        List of completions for a given testset_row
    testset_row_ids : List[str]
        List of testset_row_id for a given testset_row, is the row_id of the question a completion belongs to

    Returns
    -------
    List[Dict[str, str]] : List containing the entries into the run_row table, including columns auto-filled by supabase.
    """
    # TODO: I think the FK constraint will catch this, so we don't need to check
    # test_set_response = (
    #    supabase.table("testset_row")
    #    .select("id")
    #    .in_("id", testset_row_ids)
    #    .execute()
    # )

    # if len(test_set_response.data) != len(testset_row_ids):
    #    raise Exception("Invalid testset_row_ids")

    insert_list = [
        {
            "run_id": run_id,
            "testset_row_id": testset_row_id,
            "entity_id": entity_id,
            "pred": completion,
        }
        for completion, testset_row_id in zip(completions, testset_row_ids)
    ]
    try:
        insertion_response = supabase.table("run_row").insert(insert_list).execute()
    except APIError as e:
        if (
            e.message
            == 'insert or update on table "run_row" violates foreign key constraint "run_row_testset_row_id_fkey"'
        ):
            raise ValueError(
                f"At least one of the ids passed does not exist in the golden set"
            )

    if not insertion_response.data:
        raise Exception("Failed to insert rows")

    return insertion_response.data


# TODO: Not sure if ids is a good name.
# I think testset_row_ids is too verbose though and exposes implementation details that the user doesn't need to know
# TODO: kwargs and errors arent implemented
@init_required
def log_run(
    ids: List[str],
    completions: List[str],
    kwargs: List[dict] | None = None,
    errors: List[str | None] | None = None,
) -> Tuple[str, str]:
    """
    Log a run

    Parameters
    ----------
    ids : List[str]
        List of ids
    completions : List[str]
        List of completions
    kwargs : List[dict]
        List of kwargs
    errors : List[str | None]
        List of errors

    Returns
    -------
    run_id : str
    run_name : str
    """
    entity_id, _, task_id = _resolve_ids()

    if len(completions) != len(ids):
        raise ValueError("Length of completions and ids must be equal")

    if len(set(ids)) != len(ids):
        from collections import Counter

        raise ValueError(
            f"Found duplicate ids: {[i for i in Counter(ids).items() if i[1] > 1]}"
        )

    run_id = _create_run(run_name=_run_name, task_id=task_id, entity_id=entity_id)

    # Populate run_row table with completions and testset_row_ids
    inserted_data = _populate_rows(
        entity_id=entity_id,
        run_id=run_id,
        completions=completions,
        testset_row_ids=ids,
    )

    return run_id, _run_name


@init_required
def extend_golden_set(path: str) -> bool:
    abs_path = os.path.abspath(path)
    filename = os.path.basename(abs_path)
    upload_file = {"file": (filename, open(abs_path, "rb"), "text/csv")}
    url = f"{BASE_URL}/extend_gs"
    params = {
        "entity": "DUMMY_ENTITY",
        "project": _project_name,
        "task": _task_name,
    }
    response = requests.put(url, files=upload_file, params=params)
    return response.json()


@init_required
def delete_golden_set() -> bool:
    url = f"{BASE_URL}/delete_gs"
    params = {
        "entity": "DUMMY_ENTITY",
        "project": _project_name,
        "task": _task_name,
    }
    response = requests.post(url, params=params)
    return response.json()


@init_required
def log_model(
    model: GenerationMixin,
    tokenizer: PreTrainedTokenizer,
    generation_kwargs: Optional[Dict] = None,
):
    """
    Run the golden set through the `model` and record the results.

    :param model: The HuggingFace model to log
    :param tokenizer: The tokenizer of the `model`
    :param generation_kwargs: Optional arguments to pass to `model.generate`
    """
    generation_kwargs = generation_kwargs or dict()
    generation_kwargs.update({"return_dict_in_generate": True, "output_scores": True})

    gs_prompts = [q_a_pair[0] for q_a_pair in get_golden_set()]
    inputs_tokenized = tokenizer(gs_prompts, return_tensors="pt", padding=True)

    outputs = model.generate(**inputs_tokenized, **generation_kwargs)
    out_seq, out_scores = outputs.sequences, outputs.scores

    completions: List[str] = []
    completions_tokens: List[torch.Tensor] = []
    for prompt, output in zip(gs_prompts, out_seq):
        prompt_len = len(tokenizer.encode(prompt, return_tensors="pt")[0])
        # chop off the prompt
        completions_tokens.append(output[prompt_len:])
        completion = tokenizer.decode(output[prompt_len:])
        completions.append(completion)

    transition_scores = model.compute_transition_scores(
        out_seq, out_scores, normalize_logits=True
    )

    # chop off scores of the padding tokens
    transition_scores_no_padding = []
    for scores, completion in zip(transition_scores, completions_tokens):
        padding_len = torch.sum(completion != tokenizer.pad_token_id).item()
        transition_scores_no_padding.append(scores[:padding_len].tolist())

    # send to webapp
    url = f"{BASE_URL}/log_model"
    rundata = {
        "name": _run_name,
        "completions": completions,
        "time": "2023-11-07T19:26:19.793Z",  # dummy datetime
    }
    data = {
        "rundata": rundata,
        "logprobs": transition_scores_no_padding,
    }
    params = {
        "entity": "DUMMY_ENTITY",
        "project": _project_name,
        "task": _task_name,
    }
    response = requests.put(url, params=params, json=data)
    return response.json()


@init_required
def delete_run():
    raise NotImplementedError("Please delete runs using the webapp")
