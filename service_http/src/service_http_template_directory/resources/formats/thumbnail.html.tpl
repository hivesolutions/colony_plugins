<div class="thumbnail-view">
    ${foreach item=directory_entry from=directory_entries}
        <div class="item ${out value=directory_entry.type xml_escape=True /}-large">
            <p class="name">
                <a href="${out value=directory_entry.name quote=True xml_escape=True /}">${out value=directory_entry.name xml_escape=True /}</a>
            </p>
        </div>
    ${/foreach}
</div>
