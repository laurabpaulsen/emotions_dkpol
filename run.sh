# create environment
python3.8 -m venv .venv

# activate environment
source .venv/bin/activate

# get newsFluxus package from Centre for humanities computing
git clone https://github.com/centre-for-humanities-computing/newsFluxus.git

# install dependencies
pip install -r newsFluxus/requirements.txt
pip install -r requirements.txt

# create json file with information about the parties
python create_party_info.py

# scrape twitter
python src/scrape_twitter.py

# clean data
python src/clean_data.py

# emotion classification
python src/emotion_classification.py

# summarize emotions script from emoDynamics 
python src/summarize_emotions.py --filepath data/preprocessed/dk_pol_data_emotions.csv --output_name emotions_summarized --emotion_col emotion --time_col date_created 

# use newsFluxus to get novelty, resonnance and transience
python src/emotion_fluxus.py --filenames emotions_summarized_date
python src/emotion_fluxus.py --filenames emotions_summarized_date_hour

# create plots
python src/generate_plots.py