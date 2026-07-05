from src.analyzer import OrderAnalyzer

def main():
   
    analyzer = OrderAnalyzer()
    success, errors = analyzer.run_batch_analysis()

    print("Загруженных файлов:", success)
    print("Файлов с ошибками:", errors)

if __name__ == "__main__":
    main()
