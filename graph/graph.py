from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import END, StateGraph

from graph.consts import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEBSEARCH
from graph.nodes import generate, grade_documents, retrieve, web_search
from graph.state import  GraphState


def decide_to_generate(state):
    print("============ASSESS GRADED DOCUMENTS===============")

    if state['web_search']:
        print(
            "================DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO QUESTION, INCLUDE WEB_SEARCH========================="
        )
        return WEBSEARCH
    else:
        print("===============decision: GENERATE====================")
        return GENERATE


workflow = StateGraph(GraphState)



# add all the nodes
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

# add edges
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,  # condition node
    decide_to_generate,  # condition
            {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE
    }
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

# starting point
workflow.set_entry_point(RETRIEVE)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")