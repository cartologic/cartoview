/**
 * Created by kamal on 2/13/17.
 */
(function () {
    var currentVersion = "{{current_version}}",
        latestVersion = "{{latest_version}}";
    const check=compareVersions(currentVersion, latestVersion);
    if(check===-1){
        document.write("<div class='alert alert-danger' style='position: fixed;bottom: 0;right: 10px;z-index: 9999;'>A new version of cartoview is available for dowonload, Please upgrade</div>")
    }

})();
