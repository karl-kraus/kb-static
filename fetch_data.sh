# bin/bash

echo "fetching transkriptions from data_repo"
rm -rf data/
curl -LO https://github.com/karl-kraus/kb-data/archive/refs/heads/main.zip
unzip main

mv ./kb-data-main/data/ .

rm main.zip
rm -rf ./kb-data-main

echo "fetch imprint"
./shellscripts/dl_imprint.sh
