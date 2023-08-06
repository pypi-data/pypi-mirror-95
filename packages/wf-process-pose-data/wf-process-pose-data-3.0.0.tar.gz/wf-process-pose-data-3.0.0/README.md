# process_pose_data

Tools for fetching, processing, visualizing, and analyzing Wildflower human pose data

## Task list

* Switch parallel overlay code back to `imap_unordered()` (for less chunky progress bars) but sort output before concatenating
* Ensure that all visual specs (colors, line widths, etc.) propagate to video overlay
* Add drawing primitive to `wf-cv-utils` for text with background
* Use new text-with-background drawing primitive for pose labels
* Add timestamp to video overlays
* Consider getting rid of `geom_render` module
* Fix up progress bars so we can have task-level and segment-level progress bars without logging in notebook
* Fix up progress bars so they work properly outside of notebook with multiprocessing
* Add indentation/labeling on segment-level progress bars
* Clean up argument ordering in `reconstruct_poses_3d_alphapose_local_time_segment`
* Add `poses_2d_json_format` option to `reconstruct_poses_3d` entry point
* Add endpoints for all processing functions
* Add ability to write locally generated object IDs to Honeycomb
* Create separate workers for uploading to Honeycomb 3D poses, 3D pose tracks, interpolated 3D pose tracks, 3D pose identification, 3D pose track identification
* Dockerize pipeline
* Set up pipeline for Airflow
* Add additional machinery for checking UWB data integrity (e.g., duplicates)
* Retool `generate_inference_metadata_reconstruct_3d_poses_alphapose_local` to exclude cameras without calibration data
* Make function to delete Honeycomb inference executions
* Make function to delete local inference metadata
* Make function to delete local 3D pose files
* Make function for deleting local 3D pose data
* Rewrite all log messages so formatting isn't called if log isn't printed
* Make functions handle empty poses (all keypoints `NaN`) more gracefully (e.g., `score_pose_pairs()`, `draw_pose_2d()`)
* Make visualization functions handle missing fields (e.g., `pose_quality`) more gracefully
* Figure out inconsistent behavior of `groupby(...).apply(...)` (under what conditions does it add grouping variables to index?)
* For functions that act on dataframes, make it optional to check dataframe structure (e.g., only one timestamp and camera pair)
* For functions than iterate over previous functions, making naming and approach consistent (e.g., always use apply?)
* Add `keypoint_categories` info to pose models in Honeycomb?
* Be consistent about whether to convert track labels to integers (where possible)
* Remove dependence on OpenCV by adding necessary functionality to `cv_utils`
* Consider refactoring split between `video_io` and `cv_utils`
* Fix up `cv_utils` Matplotlib drawing functions so that they accept an axis (or figure, as appropriate)
* Fix up handling of background image alpha (shouldn't assume white background)
* Fix up _y_ axis inversion for images (go back to `cv_utils`?)
* Add option of specifying Honeycomb client info for visualization functions that require Honeycomb
* Reinstate `sns.set()` for Seaborn plots without making it spill over into non-Seaborn plots (see [here](https://stackoverflow.com/questions/26899310/python-seaborn-to-reset-back-to-the-matplotlib))
* Refactor code in `visualize` to make it less repetitive (same pattern over and over for `[verb]_by_camera`)
* Fix up legend on pose track timelines
* Add visualization for number of poses per camera per timestamp
* Replace `cv.triangulatePoints()` to increase speed (and hopefully accuracy)
* Get pose video overlays working again (for data with track labels)
* Rewrite geom rendering functions to handle the possibility of no track labels
* Rewrite function which overlays geoms on videos so that user can specify a time span that it is a subset of the geoms and/or the video
* Make all time inputs more permissive (in terms of type/format) and make all time outputs more consistent
* Be consistent about accepting timestamp arguments in any format parseable by `pd.to_datetime()`
