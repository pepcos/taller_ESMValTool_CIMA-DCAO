# Cuando queremos poner todos los datasets disponibles de una
# variable concreta en el apartado "datasets:" de la recipe
# podemos usar este "filler" que crea un diccionario de python
# con todos los datasets disponibles y lo guarda en un .yml
# que luego podemos copiar debajo del apartado "datasets:"
# de nustra recipe.

import glob
import os
import yaml

root = "/shera/datos/CMIP/CMIP6"
exps = ["historical", "ssp585"]

vars = ["tas"] #, "tos", "pr"]
datasets_dict = {v: {} for v in vars}
for short_name in vars:
    mip_prefix = "A"
    if short_name == "tos":
        mip_prefix = "O"
    files = glob.glob(os.path.join(root, f"CMIP/*/*/historical/r1i*p*f*/{mip_prefix}mon/{short_name}/*/*/*2014*.nc"))
    for file in files:
        activity, institute, dataset, exp, ensemble, mip, short_name, grid = file.split(root)[-1].split("/")[1:-2]
        if f"{dataset}_{ensemble}" in datasets_dict[short_name]:
            if grid == "gn" and "gr" in datasets_dict[short_name][f"{dataset}_{ensemble}"]["grid"]:
                datasets_dict[short_name][f"{dataset}_{ensemble}"] = {"institute": institute, "exp": exp, "ensemble": ensemble, "mip": mip, "grid": grid, "dataset": dataset}
        else:
            datasets_dict[short_name][f"{dataset}_{ensemble}"] = {"institute": institute, "exp": exp, "ensemble": ensemble, "mip": mip, "grid": grid, "dataset": dataset}

# in exp ssp585
scenario_exp = "ssp585"
for short_name in vars:
    mip_prefix = "A"
    if short_name == "tos":
        mip_prefix = "O"
    popers = []
    for alias, meta in datasets_dict[short_name].items():
        file = glob.glob(os.path.join(root, f"ScenarioMIP/*/{meta['dataset']}/{scenario_exp}/{meta['ensemble']}/{mip_prefix}mon/{short_name}/{meta['grid']}/*/*2015*.nc"))
        if len(file) == 0:
            popers.append(alias)
    for pop in popers:
        datasets_dict[short_name].pop(pop)

# If you want to keep only the runs that exist for all vars:
aliases = set(datasets_dict[vars[0]].keys()) & set(datasets_dict[vars[1]].keys()) & set(datasets_dict[vars[2]].keys())
datasets_recipe_dict = {}
for short_name in vars:
    poper = [alias for alias in datasets_dict[short_name] if alias not in aliases]
    keys = list(datasets_dict[short_name].keys())
    for alias in keys:
        if alias not in aliases:
            datasets_dict[short_name].pop(alias, None)
        else:
            datasets_dict[short_name][alias].pop("institute", None)
            datasets_dict[short_name][alias]["exp"] = ["historical", "ssp585"]
            datasets_dict[short_name][alias]["project"] = "CMIP6"
    datasets_recipe_dict[f"datasets_{short_name}"] = list(datasets_dict[short_name].values())

with open("/home/josep.cos/es-esmvaltool/common-tools/projections/recipes/datasets_filled.yml", "w") as f:
    yaml.dump(datasets_recipe_dict, f, default_flow_style=False)