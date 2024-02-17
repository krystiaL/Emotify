.DEFAULT_GOAL := default

run_model:
	python -c "from playlist_module.preprocess_df import kaggle_preprocess; kaggle_preprocess()"

#emotion and username will be passed from other modules.Update required when they are ready.
generate:
	python -c "from playlist_module.generate_playlist import send_playlist_id; send_playlist_id(emotion='Happy',account_name='Test_function')"

get_genre:
	python -c "from playlist_module.genre import get_genre; get_genre()"
