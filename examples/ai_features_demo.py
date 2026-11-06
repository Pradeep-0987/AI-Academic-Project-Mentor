from ai_engine.mentor.chat_service import chat_with_mentor
from ai_engine.mentor.progress_analyzer import analyse_progress
from ai_engine.documents.document_generator import generate_document

def main():
    context = {
        "blueprint": {"project_title": "AI crop disease detection"},
        "progress": {"completed": ["Environment setup"], "pending": ["Dataset preparation"]}
    }
    print(chat_with_mentor("What should I do next?", context, []))
    print(analyse_progress({"phases": []}, context["progress"]))
    print(generate_document("synopsis", context))

if __name__ == "__main__":
    main()
