import os

def write_dataframe_to_csv(dataframe, filename):
    output_dir = os.path.join(os.path.dirname(__file__), '../../output')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    dataframe.to_csv(file_path, index=False)