# Reefer Predictive Maintenance Solution

This project presents an approach to develop a predictive maintenance model from Reefer container metrics events and integrate it in real time.

The content is presented [in a book view](https://jbcodeforce.github.io/refarch-reefer-ml)



## Building this booklet locally

The content of this repository is written with markdown files, packaged with [MkDocs](https://www.mkdocs.org/) and can be built into a book-readable format by MkDocs build processes.

1. Install MkDocs locally following the [official documentation instructions](https://www.mkdocs.org/#installation).
1. Install Material plugin for mkdocs:  `pip install mkdocs-material` 
2. `git clone https://github.com/jbcodeforce/refarch-reefer-ml.git` _(or your forked repository if you plan to edit)_
3. `cd refarch-reefer-ml`
4. `mkdocs serve`
5. Go to `http://127.0.0.1:8000/` in your browser.

### Pushing the book to GitHub Pages

1. Ensure that all your local changes to the `master` branch have been committed and pushed to the remote repository.
   1. `git push origin master`
2. Ensure that you have the latest commits to the `gh-pages` branch, so you can get others' updates.
	```bash
	git checkout gh-pages
	git pull origin gh-pages
	
	git checkout master
	```
3. Run `mkdocs gh-deploy` from the root refarch-reefer-ml directory.