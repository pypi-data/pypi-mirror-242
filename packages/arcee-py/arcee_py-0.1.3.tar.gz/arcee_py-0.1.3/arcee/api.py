from typing import Dict, List, Optional, Union

from arcee import config
from arcee.api_handler import make_request
from arcee.dalm import DALM, check_model_status
from arcee.schemas.routes import Route


def upload_doc(
    context: str, doc_name: str, doc_text: str, **kwargs: Dict[str, Union[int, float, str]]
) -> Dict[str, str]:
    """
    Upload a document to a context

    Args:
        context (str): The name of the context to upload to
        doc_name (str): The name of the document
        doc_text (str): The text of the document
        kwargs: Any other key:value pairs to be included as extra metadata along with your doc
    """
    doc = {"name": doc_name, "document": doc_text, "meta": kwargs}
    data = {"context_name": context, "documents": [doc]}
    return make_request("post", Route.contexts, data)


def upload_docs(context: str, docs: List[Dict[str, str]]) -> Dict[str, str]:
    """
    Upload a list of documents to a context

    Args:
        context (str): The name of the context to upload to
        docs (list): A list of dictionaries with keys "doc_name" and "doc_text"

        Any other keys in the `docs` will be assumed as metadata, and will be uploaded as such. This metadata can
            be filtered on during retrieval and generation.
    """
    doc_list = []
    for doc in docs:
        if "doc_name" not in doc.keys() or "doc_text" not in doc.keys():
            raise Exception("Each document must have a doc_name and doc_text key")

        new_doc: Dict[str, Union[str, Dict]] = {"name": doc.pop("doc_name"), "document": doc.pop("doc_text")}
        # Any other keys are metadata
        if doc:
            new_doc["meta"] = doc
        doc_list.append(new_doc)

    data = {"context_name": context, "documents": doc_list}
    return make_request("post", Route.contexts, data)


def train_dalm(
    name: str, context: Optional[str] = None, instructions: Optional[str] = None, generator: str = "Command"
) -> None:
    data = {"name": name, "context": context, "instructions": instructions, "generator": generator}
    make_request("post", Route.train_model, data)
    org = get_current_org()
    status_url = f"{config.ARCEE_APP_URL}/{org}/models/{name}/training"
    print(
        f'DALM model training started - view model status at {status_url} or with arcee.get_dalm_status("{name}")\n'
        f'When training is finished, get your DALM with arcee.get_dalm("{name}")'
    )


def get_dalm_status(id_or_name: str) -> Dict[str, str]:
    """Gets the status of a DALM training job"""
    return check_model_status(id_or_name)


def get_current_org() -> str:
    return make_request("get", Route.identity)["org"]


def get_dalm(name: str) -> DALM:
    return DALM(name)
