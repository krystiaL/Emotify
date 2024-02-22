.DEFAULT_GOAL := default

# ----------------------------------
#         LOCAL SET UP
# added by: Krystia 02/20/2024
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ----------------------------------
#         RUNNING THE MODEL
# ----------------------------------
run_model:
	python -c "from playlist_module.preprocess_df import kaggle_preprocess; kaggle_preprocess()"

#emotion and username will be passed from other modules.Update required when they are ready.
generate:
	python -c "from playlist_module.generate_playlist import send_playlist_id; send_playlist_id(emotion='Happy',account_name='Test_function')"


# ----------------------------------
#         STREAMLIT COMMANDS
#   added by: Krystia 02/20/2024
# ----------------------------------

streamlit_upload_ui:
	@streamlit run interface/ui_drafts/ux_upload.py

streamlit_img_vid:
	@streamlit run interface/ui_drafts/ux_img_vid.py

streamlit_sep_upload_ui:
	@streamlit run interface/ui_drafts/ux_separate_submit.py

streamlit_main_ui:
	@streamlit run interface/ui_main.py
# ----------------------------------
#    LOCAL INSTALL COMMANDS
#   added by: Krystia 02/20/2024
# ----------------------------------
install:
	@pip install . -U
