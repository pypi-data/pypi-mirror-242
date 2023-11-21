def file_exists(file_path):
    try:
        with open(file_path, 'r'):
            return True
    except FileNotFoundError:
        return False


def analyze_csv(fichye_csv):
    try:
        # Get the absolute path
        fichye_a = fichye_csv

        if not file_exists(fichye_a):
            raise FileNotFoundError(f"Fichye a pa ekziste: {fichye_csv}")

        with open(fichye_a, 'r') as csvfile:
            lines = csvfile.readlines()

            int_column = []
            str_column = []
            dynamic_column = []
            float_column = []

            for row in lines:
                if row.startswith('"h:m:s"') or row.startswith('"d:m:s"') or row.startswith('"deg"'):
                    continue

                columns = row.split(',')

                if len(columns) >= 4:
                    try:
                        int_value = int(columns[0].strip('"'))
                        int_column.append(int_value)
                    except ValueError:
                        int_column.append(None)

                    str_value = columns[1].strip('"')
                    str_column.append(str_value)

                    dynamic_value = columns[2].strip('"')
                    dynamic_column.append(dynamic_value)

                    try:
                        float_value = float(columns[3].strip('"'))
                        float_column.append(float_value)
                    except ValueError:
                        float_column.append(None)
                else:
                    print(f" {row.strip()} ")
            print("-----------------------------------------------------------------------------------------------------")
            print("Antye:", sum(filter(None, int_column)))
            print("-----------------------------------------------------------------------------------------------------")

            print("Chenn:", str_column)
            print("-----------------------------------------------------------------------------------------------------")

            print("Dinamik:", dynamic_column)
            print("-----------------------------------------------------------------------------------------------------")

            print("Floats:", sum(filter(None, float_column)) / len(float_column))
            print("-----------------------------------------------------------------------------------------------------")

            


    except Exception as j:
        print(f"Gen yon ere nan fichye a: {j}")


