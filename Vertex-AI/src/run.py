# run.py
import uvicorn

if __name__ == "__main__":
    print("🚀 Запуск Vertex AI Agent...")
    print("📍 http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("⏹  Для остановки нажми Ctrl+C\n")

    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )