## Mark distribution
Q1: 5 marks
Q2: 5 marks
Q3: 5 marks
Q4: 5 marks
Q5: 5 marks
Total: 25 marks



## alvaranalliya / Alliya A
Q1
- You import `grace_file` twice with different methods
- Calling `netcdf4.Dataset` is extraneous when you're already importing `Dataset` individually
- Improper indentation means the integration step does not run correctly and no plot is produced (-4 points)
- `mdb_mask` is unnecessarily multiplied twice
1/5.

Q2
- "Assuming uniform spacing" is written four times in the space of six lines.
- It is not clear why you compute both `masked_areas` and `valid_areas`
- `resampled_mdb_sm_time_series` and `tws_df_datetime` are not computed in the submitted file
- `sm_df` is never used, and not saved to a csv as the comment indicates.
0/5 code does not run because of undefined variables

Q3
- Try/except statements to find title, history and source are overkill with a static file and the values are not used in any meaningful way. Unnecessary and obviously AI generated. "Moved inside the with block" is a tell, don't leave traces of your prompts. I'm fine with AI when it could be plausibly human written, which this is not.
- Good discussion
5/5

Q4
- `aligned_sm_series` is computed but not used
- This question is also affected by `resampled_mdb_sm_time_series` and `tws_df_datetime` not being computed in the submitted file
4/5

Q5
- 10m difference in 2023 is not what the plot shows. It's closer to 10cm.
- What do you mean by "the flow"?
4.5/5

Total 15.5/25

## dejongmilou
- Please submit as a Jupyter notebook
- All images saved are blank because you are calling `plt.savefig` after `plt.show`.

Q1
- It would be better to show the mask with `pcolormesh` on line 88
- Line 101 crashes the program because `fig` is not defined.
- Units not provided on plot y axis
0/5 program crashes. I have fixed the error for future questions.

Q2
- Line 130 crashes the program because `lons2` and `lats2` are not defined
- Discussion of limitations is fine
1/5 program crashes. I have fixed the error again for future questions.

Q3
5/5

Q4
5/5

Q5
- It is unclear what plot you are referring to on lines 377-380
- It is difficult to compare the box plots when they are in separate figures with different y axes.
- You need to say something about the results of the ANOVA testing.
3/5

Total 14/25


## delveslily
- Please comment your code
- More important please indicate which question you are working on
- You can add markdown text to a jupyter notebook instead of printing your written answers.

Q1
5/5

Q2
- No discussion of data limitation
2.5/5

Q3
- Written part is obviously AI written.
5/5

Q4
- `gw_df_all` is not defined in the submitted file so no plots are produced.
0/5 code does not run

Q5
- The "long term declining trend" is not evidenced.
- The plot does not well support your argument that the north having greater variability in groundwater. Computing variances would help.
2/5

Total 14.5/25





## easterbywoodsavannah
- Please include text answers in markdown cells in the notebook.

Q1
- `Point` is not imported
- `lats` and `lons` are used before they are defined
- `decoded_times` is used before it is defined
0/5 code does not run

Q2
- Good plot, but no discussion
3/5

Q3
5/5

Q4
5/5

Q5
5/5

Total 18/25


## fifieldfred
- Please submit the .ipynb file so that I can run it.

Q1
5/5

Q2
- No discussion
2.5/5

Q3
5/5

Q4
5/5

Q5
5/5

Total 22.5/25


## gardinerbradley
Q1
5/5

Q2
5/5

Q3
- `xarray` is not imported so code does not run as submitted
3/5 submitted code does not run

Q4
0/5 not attempted

Q5
0/5 not attempted

Total 13/25


## laibutlersaskia
Q1
5/5

Q2
- No discussion
2.5/5

Q3
5/5

Q4
5/5

Q5
5/5

Total 22.5/5


## lemmjosie
- Please submit the .ipynb file so that I can make sure the code runs.

Q1
5/5

Q2
- No discussion
2.5/5

Q3
5/5

Q4
5/5

Q5
- Discussion of spatial variability is very basic
4/5

Total 21.5/25


## mannjustin
Q1
- Title says LWE but units are in m3. This does not match up.
4/5

Q2
- Yes deeper soil layers might be drier but the soil also extends past 20cm. The claim that the 20cm assumption is a gross overestimation is not well argued.
- The plot suggests that there is on the order of 50 m3 of soil moisture in the entire basin. This seems improbable (check units).
3/5

Q3
- No units on plot
4/5

Q4
- I do not believe that we have gone from the order of 1e11 m3 variability in total water storage to the order of  1e8 m3 variability in groundwater. The north/south plot makes much more sense.
4/5

Q5
5/5

Total 20/25


## mcfaddenben

Q1
- Typo on y axis label, should say km3
5/5

Q2
- No discussion
2.5/5

Q3
5/5

Q4
- North/south plots could be combined for better comparison
5/5

Q5
5/5


## meixnersarah
- Please submit your .ipynb file.

Q1
5/5

Q2
- You are using a 5cm depth assumption instead of the 20cm assumption.
- No discussion
2/5

Q3
5/5

Q4
5/5

Q5
5/5


## pascoedeclan
- It is preferred that you submit everything in one jupyter notebook
- x axes with days since grace epoch are difficult to interpret. Marking years would be preferred.

Q1
- The if statement for units is unnecessary when you're dealing with a static data type
- `MDB_total_ws` is computed but not used
5/5

Q2
- No discussion of thickness assumption
- Please comment your code
2.5/5

Q3
5/5

Q4
5/5

Q5
- Mascon-scale maps are not provided.
- Leakage near coastlines is difficult to justify as significant here since the MDB is almost all inland.
- Give years for the droughts you/the AI talk about.
3/5

Total 19.5/25


## rechnerthomasmax
Q1
- `Point` is not imported from `shapely.geometry` so the submitted code does not run.
2/5 submitted code does not run

Q2
- No discussion
- Don't write "fractional units from dataset", just write the unit.
2.5/5

Q3
5/5

Q4
- The assignment says to assume a soil depth of 20cm, but you use 10cm without justification.
4/5

Q5
- The numbers quoted in your discussion don't match those outputted by the code.
5/5

Total 18.5/25


## taibmaya
Q1
- Would have been great if you submitted the mask files
5/5

Q2
5/5

Q3
5/5

Q4
5/5

Q5
5/5

Total 25/25


## tapsfieldcharlie
Q1
5/5

Q2
- No discussion
2.5/5

Q3
5/5

Q4
5/5

Q5
- First panel of the figure is blank.
5/5

Total 22.5/25


## wilsonciara
- Please submit your .ipynb file.

Q1
- Inconsistency in your comments about whether LWE is in cm or mm
5/5

Q2
- No discussion of soil depth assumption (which would be very relevant if you integrated instead of averaging).
2.5/5

Q3
5/5

Q4
5/5

Q5
5/5


## yakemichaeljames
Q1
- I need to be able to run your code, which means submitting the .geojson file since it's not one linked to in the assignment.
3/5

Q2
5/5

Q3
5/5

Q4
5/5

Q5
- Computing variances would help make arguments about variability
4/5

Total 23/25


## yancrystal
- Please submit your .ipynb file, and it is preferred that you include written answers in markdown cells in the notebook.

Q1
- Putting everything into a function is odd structure in a notebook
5/5

Q2
5/5

Q3
5/5

Q4
- Please use line breaks to structure your code for readability
5/5

Q5
5/5

Total 25/25


## yousufzaiahmadsurosh
- Please resubmit. The file submitted links to files on your local directory.

