import pandas as pd
import config


class OrderAnalyzer:

    def __init__(self):
        self.data_dir = config.data_dir
        self.reports_dir = config.reports_dir
        self.logs_dir = config.logs_dir

        # Простое создание папок, если их нет
        self.reports_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

    def read_data(self, file_path):
        df = pd.read_csv(file_path)
        return df

    def filter_by_status(self, df):
        filtered_df = df[df["status"] == config.target_status]
        return filtered_df

    def calculate_metrics(self, df, file_name):
        total_orders = int(len(df))

        if total_orders > 0:
            total_revenue = float(df["total_amount"].sum())
            average_check = float(df["total_amount"].mean())
        else:
            total_revenue = 0.0
            average_check = 0.0

        metrics = {
            "file_name": file_name,
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "average_check": round(average_check, 2),
        }
        return metrics

    def process_single_file(self, file_path):
        raw_df = self.read_data(file_path)
        clean_df = self.filter_by_status(raw_df)
        result = self.calculate_metrics(clean_df, file_path.name)
        return result

    def run_batch_analysis(self):
        all_files = list(self.data_dir.glob("*"))
        csv_files = []
        for single_file in all_files:
                if single_file.suffix == ".csv":
                    csv_files.append(single_file))

        if not csv_files:
            print("CSV файлов не найдено")
            return 0, 0

        all_reports = []
        success_count = 0
        error_count = 0

        for file_path in csv_files:
            try:
                file_metrics = self.process_single_file(file_path)
                all_reports.append(file_metrics)
                success_count += 1
            except Exception as error:
                log_path = self.logs_dir / config.log_file

                file_log = open(log_path, "w", encoding="utf-8")
                file_log.write(f"Ошибка в файле {file_path.name}: {str(error)}\n")
                file_log.close()

                error_count +=1

        if len(all_reports) > 0:
            final_df = pd.DataFrame(all_reports)
            report_path = self.reports_dir / config.report_file
            final_df.to_csv(report_path, index=False)

        return success_count, error_count
