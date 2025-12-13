from typing import Any, Dict
import asyncio
from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState


async def grade_single_document(question: str, doc: Any) -> tuple[Any, str]:
    """
    Grade a single document asynchronously.
    
    Args:
        question: The user question
        doc: Document to grade
        
    Returns:
        Tuple of (document, grade)
    """
    score = await retrieval_grader.ainvoke(
        {"question": question, "document": doc.page_content}
    )
    return doc, score.binary_score


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question.
    Grades all documents in parallel for better performance.
    If any document is not relevant, we will set a flag to run web search.
    
    Args:
        state (dict): the current graph state

    Returns:
        state (dict): filtered out irrelevant documents and updated web_search state
    """
    print("========CHECK DOCUMENT RELEVANCE TO QUESTION=============")
    question = state["question"]
    documents = state["documents"]

    # Grade all documents in parallel
    async def grade_all():
        tasks = [grade_single_document(question, doc) for doc in documents]
        return await asyncio.gather(*tasks)
    
    # Run the async grading
    results = asyncio.run(grade_all())
    
    # Process results
    filtered_docs = []
    web_search = False
    
    for doc, grade in results:
        if grade.lower() == "yes":
            print("============GRADE: DOCUMENT RELEVANT=====================")
            filtered_docs.append(doc)
        else:
            print("===========GRADE: DOCUMENT NOT RELEVANT=================")
            web_search = True
    
    return {"document": filtered_docs, "question": question, "web_search": web_search}
