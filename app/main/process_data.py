import pandas as pd
import numpy as np
from treecover.retrieve_sentinel_csv import fetch_data

from joblib import load

libsqlite_path = '../../treecover/libsqlitefunctions.so'
model_path = "treecover/model_sentinel_logtrans_stratified_huber_3months_2000_60leaves.joblib"
model_path_2 = "treecover/model_landsat_median_sds.joblib"
diff_to_colour = {0.0: "success", 0.1: "success", 0.2: "info", 0.3: "info", 0.4: "warning", 0.5: "warning"}


def process_file(file, choice):
    data = pd.read_csv(file)
    
    if choice == "Model2":
        regions = ["CentralAsia","EastSouthAmerica","Europe","HornAfrica","MiddleEast","NorthAmerica","NorthernAfrica","Sahel","SouthWestAsia","SouthernAfrica","WestSouthAmerica"]
        aridity = ["Dry subhumid","Hyperarid","Semiarid"]
        for i in regions:
            data["dryland_assessment_region_"+i] = np.where(data["dryland_assessment_region"].str.contains(i), 1, 0)

        for j in aridity:
            data["Aridity_zone_"+j] = np.where(data["Aridity_zone"].str.contains(j), 1, 0)

        data = data.drop(["dryland_assessment_region"], axis=1)
        data = data.drop(["Aridity_zone"], axis=1)

    data["predicted"] = get_prediction(data, choice)  # np.round(np.random.rand(len(data), 1), 3)
    data["predicted"] = np.round(1/(1+np.exp(-data["predicted"])),2)
    for key in ["longitude", "latitude"]:
        data[key] = np.round(data[key], 7)
    data["diff"] = data.apply(lambda row: np.round(np.abs(row["tree_cover"] - row["predicted"]), 1), axis=1)
    data["class"] = data.apply(lambda row: diff_to_colour.get(row["diff"], "danger"), axis=1)
    data.sort_values(by="diff", inplace=True, ascending=False)
    return data[["class", "plot_id", "longitude", "latitude", "tree_cover", "predicted"]]


def get_prediction(data, choice):
    feat = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11', 'sr_aerosol',
       'pixel_qa', 'radsat_qa', 'B1_sd', 'B2_sd', 'B3_sd', 'B4_sd', 'B5_sd',
       'B6_sd', 'B7_sd', 'B10_sd', 'B11_sd', 'sr_aerosol_sd', 'pixel_qa_sd',
       'radsat_qa_sd', 'dryland_assessment_region_CentralAsia',
       'dryland_assessment_region_EastSouthAmerica',
       'dryland_assessment_region_Europe',
       'dryland_assessment_region_HornAfrica',
       'dryland_assessment_region_MiddleEast',
       'dryland_assessment_region_NorthAmerica',
       'dryland_assessment_region_NorthernAfrica',
       'dryland_assessment_region_Sahel',
       'dryland_assessment_region_SouthWestAsia',
       'dryland_assessment_region_SouthernAfrica',
       'dryland_assessment_region_WestSouthAmerica',
       'Aridity_zone_Dry subhumid', 'Aridity_zone_Hyperarid',
       'Aridity_zone_Semiarid']

    needed_cols = ['longitude', 'latitude', 'Aridity_zone', 'tree_cover']
    excluded_cols = ['longitude','latitude','dryland_assessment_region','land_use_category','tree_cover', 'plot_id']
    
    if choice == "Model1":
        model = load(model_path)
        data.Aridity_zone = pd.Categorical(data.Aridity_zone)
        if len(data.columns) < 278 and all([x in data.columns for x in needed_cols]):
            print('Valid input file but features not given - will fetch them.')
            data = fetch_data(data, None, libsqlite_path)
        return np.round(model.predict(data[data.columns.difference(excluded_cols)]), 3)
    else:
        model = load(model_path_2)
        return np.round(model.predict(data[feat]), 3)
