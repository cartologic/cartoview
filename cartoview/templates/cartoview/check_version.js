/**
 * Created by kamal on 2/13/17.
 */
(function () {
    var currentVersion = "{{current_version}}",
        latestVersion = "{{latest_version}}";
    const el="<div class='alert alert-danger' style='position: fixed;bottom: 0;right: 10px;z-index: 9999;'>A new version(v "+latestVersion+") of cartoview is available for dowonload, Please upgrade. Installed Version(v "+currentVersion+")</div>"
    const check=compareVersions(currentVersion, latestVersion);
    if(check===-1){
        document.write(el)
    }

})();
