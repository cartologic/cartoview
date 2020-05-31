(function () {
  var app = angular.module("cartoview.appManager.manager", [
    "cartoview.appManager.resources",
    "ui.bootstrap",
    "dndLists",
  ]);

  app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = "csrftoken";
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
  });
  app.directive("dynamicTemplate", function ($compile) {
    return {
      restrict: "A",
      scope: {
        context: "=",
        template: "=",
      },
      controller: function ($scope, $element, $compile) {
        $scope.$watch(
          function () {
            return $scope.context;
          },
          function () {
            if ($scope.context) {
              $element.html($scope.template);
              angular.extend($scope, $scope.context);
              $compile($element.contents())($scope);
            }
          }
        );
      },
    };
  });

  app.directive("appsReorder", function ($compile) {
    return {
      restrict: "E",
      templateUrl: "apps-reorder.html",
      scope: {
        installedApps: "=",
      },
    };
  });
  app.service("Dialogs", function ($uibModal, $log, $document) {
    this.confirm = function (options) {
      var controller = function ($scope, $uibModalInstance) {
        options.template = options.template || "{{msg}}";
        $scope.options = options;
        options.okText = options.okText || "Ok";
        $scope.ok = function () {
          $uibModalInstance.close(true);
        };
        $scope.cancel = function () {
          $uibModalInstance.dismiss("cancel");
        };
      };
      var modalInstance = $uibModal.open({
        animation: true,
        templateUrl: "confirm-dialog.html",
        controller: controller,
      });

      return modalInstance.result;
    };
  });
  app.service("Alerts", function () {
    var service = this;
    this.alerts = [];
    this.addAlert = function (alert) {
      service.alerts.push(alert);
    };

    this.closeAlert = function (index) {
      service.alerts.splice(index, 1);
    };
    this.closeAll = function () {
      service.alerts = [];
    };
  });
  app.service("AppInstaller", function ($http, urls) {
    var service = this;
    // get the apps required to install this app
    var _getDependencies = function (app, appsHash, dependencies) {
      angular.forEach(app.latest_version.dependencies, function (
        version,
        name
      ) {
        if (appsHash[name] && appsHash[name].installedApp) {
          if (appsHash[name].installedApp.version < version) {
            dependencies.push({
              name: name,
              version: version,
              upgrade: true,
            });
            _getDependencies(appsHash[name], appsHash, dependencies);
          }
        } else {
          dependencies.push({
            name: name,
            version: version,
            upgrade: false,
          });
          _getDependencies(appsHash[name], appsHash, dependencies);
        }
      });
      return dependencies;
    };
    this.getDependencies = function (app, appsHash) {
      return _getDependencies(app, appsHash, []);
    };

    var _getDependents = function (app, appsHash, dependents) {
      angular.forEach(app.store.installedApps.objects, function (installedApp) {
        var currentApp = appsHash[installedApp.name];
        // NOTE:this line will raise an error while uninstalling app
        // It was working fine before this commit in gitlab f976590bd981b05f062f055f1aed3040b190f8e9
        // I this our app market result for apps was changed without handle this change here
        if (currentApp) {
          if (
            dependents.indexOf(currentApp) == -1 &&
            currentApp.latest_version.dependencies[app.name]
          ) {
            dependents.push(currentApp);
            _getDependents(currentApp, appsHash, dependents);
          }
        }
      });
      return dependents;
    };
    // get the apps that depend on this app.
    // must be called before app uninstall
    this.getDependents = function (app, appsHash) {
      return _getDependents(app, appsHash, [app]);
    };
    this.install = function (app) {
      var url = urls.BULK_INSTALL;
      const data = {
        apps: [
          {
            app_name: app.name,
            version: app.latest_version.version,
            store_id: app.store.id,
          },
        ],
        restart: false,
      };
      return $http.post(url, data);
    };
    this.uninstall = function (app) {
      var url = "../uninstall/" + app.store.id + "/" + app.name + "/";
      return $http.post(url);
    };
    this.restart = function () {
      var url = urls.RESTART_SERVER;
      return $http.get(url);
    };
    this.pingServer = function () {
      var url = "/";
      return $http.get(url);
    };
  });
  app.directive("alertsPanel", function () {
    return {
      restrict: "E",
      transclude: true,
      replace: true,
      scope: {
        messages: "=",
      },
      template: [
        "<div class='alerts-ct'>",
        "<div uib-alert ng-repeat='msg in messages'",
        "ng-class='getCls(msg.type)' close='messages.splice($index, 1)'>",
        "{{msg.msg}}",
        "</div>",
        "</div>",
      ].join(""),
      controller: function ($scope) {
        var classes = {
          error: "alert-danger",
        };
        $scope.getCls = function (type) {
          return "alert " + (classes[type] || "alert-warning");
        };
      },
    };
  });
  app.directive("cartoviewAppInstaller", function () {
    return {
      restrict: "E",
      transclude: true,
      replace: true,
      templateUrl: "app-installer.html",
      controller: function (
        $scope,
        InstalledAppResource,
        AppStoreResource,
        AppStore,
        AppInstaller,
        Dialogs,
        $timeout,
        Alerts
      ) {
        $scope.selectedStoreId = null;
        var appsHash = {};
        $scope.loading = true;
        $scope.appsErrors = [];
        $scope.storeError = false;
        $scope.busy = false;
        $scope.compatible = function (cartoviewVersions) {
          var compatible = false;
          for (var i = 0; i < cartoviewVersions.length; i++) {
            const version = cartoviewVersions[i].version;
            const current_version_check = compareVersions(
              version,
              versionInfo.current_version
            );
            var backward_version_check = -1;
            for (var j = 0; j < versionInfo.backward_versions.length; j++) {
              const v = versionInfo.backward_versions[j];

              if (compareVersions(version, v) == 0) {
                backward_version_check = 0;
                break;
              }
            }
            if (current_version_check === 0 || backward_version_check === 0) {
              compatible = true;
              break;
            }
          }
          return compatible;
        };
        $scope.upgradable = function (currentVersion, storeVersion) {
          var compatible = false;
          if (compareVersions(currentVersion, storeVersion) === -1) {
            compatible = true;
          }
          return compatible;
        };
        $scope.stores = AppStoreResource.query(function () {
          $scope.stores.objects.forEach(function (store) {
            if ($scope.stores.objects.length > 0) {
              $scope.selectedStoreId = $scope.stores.objects[0].id;
            }
            store.update = function (callback, persist) {
              var params = {
                store_id: store.id,
                t: new Date().getTime(), //to force server request
              };
              store.installedApps = InstalledAppResource.query(
                params,
                function () {
                  if (store._apps && store._apps.objects) {
                    store._apps.objects.forEach(function (app) {
                      delete app.installedApp;
                    });
                  }
                  store.installedApps.objects.forEach(function (installedApp) {
                    if (appsHash[installedApp.name]) {
                      appsHash[installedApp.name].installedApp = installedApp;
                    }
                  });
                  if (typeof callback == "function") {
                    callback();
                  }
                },
                function () {
                  //keep requesting until server responds
                  if (persist) {
                    $timeout(function () {
                      store.update(callback, persist);
                    }, 2000);
                  }
                }
              );
              $scope.loading = false;
            };
            Object.defineProperty(store, "apps", {
              configurable: true,
              get: function () {
                if (!this._apps) {
                  this._apps = AppStore.AppResource(this).query(function () {
                    store._apps.objects.forEach(function (app) {
                      appsHash[app.name] = app;
                      app.store = store;
                    });
                    store.update();
                  });
                  this._apps.$promise.catch(function (errorResponse) {
                    // console.error(errorResponse);
                    $scope.loading = false;
                    $scope.storeError = true;
                  });
                }
                return this._apps;
              },
            });
          });
        });
        $scope.getSelectedStore = function () {
          var selected;
          if ($scope.selectedStoreId) {
            $scope.stores.objects.forEach(function (store) {
              if (store.id == $scope.selectedStoreId) {
                selected = store;
                return false;
              }
            });
          }
          return selected;
        };
        //
        var updateStore = function (store) {
          $scope.restarting = true;
          //wait for 5 seconds to insure that the server starts the restarting process
          $timeout(function () {
            store.update(function () {
              $scope.restarting = false;
              $scope.installing = null;
            }, true);
          }, 5000);
        };

        function install(requiredApp) {
          $scope.installing = requiredApp;
          $scope.appsErrors = [];
          AppInstaller.install(requiredApp)
            .success(function (res) {
              res.forEach(function (appResult) {
                if (appResult.success) {
                  // updateStore(requiredApp.store);
                  // Just update the store without waiting for the server to restart
                  requiredApp.store.update(undefined, true);
                  $scope.installing = null;
                } else {
                  const msgData = {
                    type: appResult.success ? "success" : "danger",
                    msg: appResult.app_name + ": " + appResult.message,
                  };
                  $scope.appsErrors.push(msgData);
                }
              }, this);
            })
            .error(function (res, status) {
              $scope.installing = null;
              if (status == -1) {
                var error = "Cannot connect to the server";
                app.messages.push({
                  type: "danger",
                  msg: error,
                });
              } else if (status >= 400) {
                var error = "Cannot install app " + app.title;
                app.messages.push({
                  type: "danger",
                  msg: error,
                });
              }

              if (Array.isArray(res)) {
                res.forEach(function (message) {
                  const msgData = {
                    type: message.success ? "success" : "danger",
                    msg: message.app_name + ": " + message.message,
                  };
                  $scope.appsErrors.push(msgData);
                }, this);
              }
              if (res.error_message) {
                const msgData = {
                  type: "danger",
                  msg: res.error_message,
                };
                $scope.appsErrors.push(msgData);
              }
              console.log($scope.appsErrors);
            });
        }
        $scope.install = function (app, upgrade) {
          var dependencies = AppInstaller.getDependencies(app, appsHash);
          if (dependencies.length > 0) {
            Dialogs.confirm({
              title: "App dependencies",
              template: [
                "<strong>This app requires the following apps to be installed</strong><br>",
                "<ul class='list-group'><li class='list-group-item' ng-repeat='d in dependencies'>",
                "{{appsHash[d.name].title}} ",
                "<span class='label label-info'>v{{d.version}}</span>",
                "<span ng-if='d.upgrade'>(v{{appsHash[d.name].installedApp.version}} is installed)</span>",
                "</li></ul>",
                "<div>Install Them?</div>",
              ].join(""),
              dependencies: dependencies,
              appsHash: appsHash,
            }).then(function (confirm) {
              if (confirm) {
                install(app);
              }
            });
          } else {
            install(app);
          }
        };

        var uninstall = function (app) {
          $scope.installing = app;
          AppInstaller.uninstall(app)
            .success(function (res) {
              // updateStore(app.store);
              // just update the store without waiting for the server to restart
              app.store.update(undefined, true);
              $scope.installing = null;
            })
            .error(function () {
              $scope.installing = null;
              app.error = "Unable to uninstall";
            });
        };

        var setActive = function (app, active) {
          var action = active ? "activate" : "suspend";
          InstalledAppResource[action](
            {
              appId: app.installedApp.id,
            },
            function (res) {
              if (res.success) {
                app.installedApp.active = active;
              }
            }
          );
        };
        $scope.toggleActive = function (app) {
          setActive(app, !app.installedApp.active);
        };

        $scope.uninstall = function (app) {
          var dependents = AppInstaller.getDependents(app, appsHash);
          if (dependents.length > 0) {
            Dialogs.confirm({
              title: "Uninstall app",
              template: [
                "<strong>This will uninstall the following apps</strong>",
                "<ul class='list-group'><li class='list-group-item' ng-repeat='d in dependents'>",
                "{{appsHash[d.name].title}} ",
                "<span class='label label-info'>v{{appsHash[d.name].installedApp.version}}</span>",

                "</li></ul>",
                "<div>Do you want to proceed?</div>",
              ].join(""),
              dependents: dependents,
              appsHash: appsHash,
            }).then(function (confirm) {
              if (confirm) {
                uninstall(app);
              }
            });
          } else {
            uninstall(app);
          }
        };

        $scope.reorder = function () {
          var installedApps = $scope.getSelectedStore().installedApps.objects;
          Dialogs.confirm({
            okText: "Save Order",
            title: "Reorder Installed Apps",
            template:
              "<apps-reorder installed-apps='installedApps'></apps-reorder>",
            installedApps: installedApps,
          }).then(function (confirm) {
            if (confirm) {
              var apps = [];
              installedApps.forEach(function (app) {
                apps.push(app.id);
              });
              var params = {
                apps: apps,
              };
              InstalledAppResource.reorder(params, function (res) {
                console.debug(res);
              });
            }
          });
        };
        $scope.restart = function () {
          $scope.appsErrors = [];
          $scope.restarting = true;
          var restarted = false;
          AppInstaller.restart().error(function (res, status) {
            if (status == 500) {
              $scope.restarting = false;
              const msgData = {
                type: "danger",
                msg: "Failed to restart Server",
              };
              $scope.appsErrors.push(msgData);
              restarted = true;
            }
          });

          function waitForRestart() {
            AppInstaller.pingServer()
              .success(function (res) {
                restarted = true;
                $scope.restarting = false;
                location.reload()
              })
              .error(function (res, status) {
                if (status == 500) {
                  $scope.restarting = false;
                  const msgData = {
                    type: "danger",
                    msg: "Failed to restart Server",
                  };
                  $scope.appsErrors.push(msgData);
                  restarted = true;
                }
              });
            if (!restarted) {
              $timeout(function () {
                waitForRestart();
              }, 10000);
            }
          }
          $timeout(function () {
            waitForRestart();
          }, 10000);
        };
        $scope.showRestartPanel = function () {
          var installedApps = $scope.getSelectedStore().installedApps.objects;
          if(installedApps)
          return installedApps.findIndex(function (app) {
            return app.pending
          }) !== -1
          return false
        };
      },
    };
  });
})();
