<div id="wiki-page-edit-container">
    <div id="wiki-page-edit">
        <form action="update" id="wiki-page-edit-form" method="post">
            <input name="page[name]" type="hidden" value="${out_none value=page_name /}" />
            <div class="wiki-page-edit-line">
                <div class="warning">For help regarding the wiki syntax please refer to <a href="documentation_demo.html">reference</a>.</div>
            </div>
            <div class="wiki-page-edit-line">
                <div id="wiki-controls">
                    <div id="wiki-controls-icons">
                        <div class="wiki-control-icon wiki-control-icon-bold"></div>
                        <div class="wiki-control-icon wiki-control-icon-italic"></div>
                        <div class="wiki-control-icon wiki-control-icon-quote"></div>
                    </div>
                </div>
                <textarea id="wiki-page-edit-contents-text-area" name="page[contents]" class="wiki-text-area">${out_none value=page_source /}</textarea>
            </div>
            <div class="wiki-page-edit-line">
                <input id="wiki-page-edit-summary-input" name="page[summary]" class="wiki-input" type="text" value="Describe your change" current_status="" original_value="Describe your change" />
            </div>
            <div id="wiki-page-edit-buttons" class="wiki-page-edit-line">
                <div id="wiki-page-edit-publish-button" class="wiki-button wiki-button-blue">Publish</div>
                <div id="wiki-page-edit-preview-button" class="wiki-button wiki-button-blue">Preview</div>
            </div>
        </form>
    </div>
</div>

${out_none value=page_contents /}
