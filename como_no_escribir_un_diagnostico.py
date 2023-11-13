import iris
import sys
import yaml

import matplotlib.pyplot as plt
import iris.quickplot as qplt

def main(settings):
    with open(settings, "r") as f:
        settings_dict = yaml.full_load(f)

    metadata_paths = settings_dict["input_files"]
    metadata = []
    for metadata_path in metadata_paths:
        with open(metadata_path) as f:
            metadata.append(yaml.full_load(f))

    # MultiModelMean campo de temperaturas
    for intermediary_files_meta in metadata:
        for file_meta in intermediary_files_meta.values():
            if file_meta["dataset"] == "MultiModelMean" and file_meta["variable_group"] == "tas_clim_global":
                cube = iris.load_cube(file_meta["filename"])
    print(cube)
    plt.figure()
    qplt.pcolormesh(cube)
    plt.gca().coastlines()
    plt.savefig(f"{settings_dict['plot_dir']}/global_map.png")

if __name__ == '__main__':
    settings = sys.argv[1]
    main(settings)