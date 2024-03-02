.DEFAULT_GOAL := default

default: pytest

# default: pylint pytest

# pylint:
# 	find . -iname "*.py" -not -path "./tests/test_*" | xargs -n1 -I {}  pylint --output-format=colorized {}; true

pytest:
	echo "no tests"

# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         HEROKU COMMANDS
# ----------------------------------

streamlit_main_ui:
	-@streamlit run app.py --server.port 8504

# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------
install:
	@pip install . -U

clean:
	@rm -fr */__pycache__
	@rm -fr __init__.py
	@rm -fr build
	@rm -fr dist
	@rm -fr *.dist-info
	@rm -fr *.egg-info
	-@rm model.joblib


###playlist_module start###
#Extract user data
get_genre:
	python -c "from playlist_module.genre import get_genre; get_genre()"

#Create a database labeled with emotions
run_model:
	python -c "from playlist_module.preprocess_df import df_preprocess; df_preprocess()"

#Generate new playlist
#emotion and username will be passed from other modules.Update required when they are ready.
generate:
	python -c "from playlist_module.generate_playlist import send_playlist_id; send_playlist_id(account_name='Test_function')"

###playlist_module end###
