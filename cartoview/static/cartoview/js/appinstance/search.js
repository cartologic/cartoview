/**
 * Created by kamal on 9/22/16.
 */
'use strict';

(function () {
    var module = angular.module('geonode_main_search');
    module.load_apps = function ($http, $rootScope, $location) {
        var params = typeof FILTER_TYPE == 'undefined' ? {} : {
            'type': FILTER_TYPE
        };
        params['single_instance'] = false
        if ($location.search().hasOwnProperty('app__name')) {
            const oldVal = $location.search()['app__name']
            $location.search('app__name', null)
            $location.search('app__name__in', oldVal)
        }
        if ($location.search().hasOwnProperty('app__title')) {
            $location.search('app__title', null)
        }
        if ($location.search().hasOwnProperty('app_name__in')) {

            params['app_name__in'] = $location.search()['app__name__in'];
        }
        $http.get(APPS_ENDPOINT, {
            params: params
        }).then(function (data) {
            if ($location.search().hasOwnProperty('app__name__in')) {
                data.objects = module.set_initial_filters_from_query(data.data.objects,
                    $location.search()['app__name__in'], 'identifier');
            }
            $rootScope.apps = data.objects;
            if (HAYSTACK_FACET_COUNTS && $rootScope.query_data) {
                module.haystack_facets($http, $rootScope, $location);
            }
        });
    };

    /*
    * Load categories and keywords
    */
    module.run(function ($http, $rootScope, $location) {
        /*
        * Load categories and keywords if the filter is available in the page
        * and set active class if needed
        */
        if ($('#categories').length > 0) {
            module.load_categories($http, $rootScope, $location);
        }

        if ($('#group-categories').length > 0) {
            module.load_group_categories($http, $rootScope, $location);
        }

        //if ($('#keywords').length > 0){
        //   module.load_keywords($http, $rootScope, $location);
        //}
        module.load_h_keywords($http, $rootScope, $location);

        if ($('#regions').length > 0) {
            module.load_regions($http, $rootScope, $location);
        }
        if ($('#owners').length > 0) {
            module.load_owners($http, $rootScope, $location);
        }
        if ($('#groups').length > 0) {
            module.load_groups($http, $rootScope, $location);
        }
        if ($('#tkeywords').length > 0) {
            module.load_t_keywords($http, $rootScope, $location);
        }
        if ($('#apps').length > 0) {
            module.load_apps($http, $rootScope, $location);
        }


        // Activate the type filters if in the url
        if ($location.search().hasOwnProperty('type__in')) {
            var types = $location.search()['type__in'];
            if (types instanceof Array) {
                for (var i = 0; i < types.length; i++) {
                    $('body').find("[data-filter='type__in'][data-value=" + types[i] + "]").addClass('active');
                }
            } else {
                $('body').find("[data-filter='type__in'][data-value=" + types + "]").addClass('active');
            }
        }

        // Activate the sort filter if in the url
        if ($location.search().hasOwnProperty('order_by')) {
            var sort = $location.search()['order_by'];
            $('body').find("[data-filter='order_by']").removeClass('selected');
            $('body').find("[data-filter='order_by'][data-value=" + sort + "]").addClass('selected');
        }

    });

    module.controller('geonode_search_controller', function ($injector, $scope, $location, $http, Configs) {
        $scope.query = $location.search();
        $scope.query.limit = $scope.query.limit || CLIENT_RESULTS_LIMIT;
        $scope.query.offset = $scope.query.offset || 0;
        $scope.page = Math.round(($scope.query.offset / $scope.query.limit) + 1);

        //Get data from apis and make them available to the page
        function query_api(data) {
            // TODO: find better way to just inject app data.
            $http.get(APPS_ENDPOINT, {
                params: {
                    name: data.app__name__in
                }
            }).then(function (res) {
                if (res.data.objects.length > 0) {
                    $scope.app_name = res.data.objects[0].name;
                    $scope.appTitle = res.data.objects[0].title;
                } else {
                    $scope.appTitle = data.app__name__in;
                }
            });
            $http.get(Configs.url, {params: data || {}}).then(successCallback, errorCallback);

            function successCallback(data) {
                //success code
                setTimeout(function () {
                    $('[ng-controller="CartList"] [data-toggle="tooltip"]').tooltip();
                }, 0);
                $scope.results = data.data.objects;
                $scope.total_counts = data.data.meta.total_count;
                $scope.$root.query_data = data.data;
                if (HAYSTACK_SEARCH) {
                    if ($location.search().hasOwnProperty('q')) {
                        $scope.text_query = $location.search()['q'].replace(/\+/g, " ");
                    }
                } else {
                    if ($location.search().hasOwnProperty('title__icontains')) {
                        $scope.text_query = $location.search()['title__icontains'].replace(/\+/g, " ");
                    }
                    if ($location.search().hasOwnProperty('name__icontains')) {
                        $scope.text_query = $location.search()['name__icontains'].replace(/\+/g, " ");
                    }
                    if ($location.search().hasOwnProperty('name')) {
                        $scope.text_query = $location.search()['name'].replace(/\+/g, " ");
                    }
                }

                //Update facet/keyword/category counts from search results
                if (HAYSTACK_FACET_COUNTS) {
                    try {
                        module.haystack_facets($http, $scope.$root, $location);
                        $("#types").find("a").each(function () {
                            if ($(this)[0].id in data.data.meta.facets.subtype) {
                                $(this).find("span").text(data.data.meta.facets.subtype[$(this)[0].id]);
                            } else if ($(this)[0].id in data.data.meta.facets.type) {
                                $(this).find("span").text(data.data.meta.facets.type[$(this)[0].id]);
                            } else {
                                $(this).find("span").text("0");
                            }
                        });
                    } catch (err) {
                        // console.log(err);
                    }
                }
            };

            function errorCallback(error) {
                //error code
            };
        };
        query_api($scope.query);

        /*
        * Pagination
        */
        // Control what happens when the total results change
        $scope.$watch('total_counts', function () {
            $scope.numpages = Math.round(
                ($scope.total_counts / $scope.query.limit) + 0.49
            );

            // In case the user is viewing a page > 1 and a
            // subsequent query returns less pages, then
            // reset the page to one and search again.
            if ($scope.numpages < $scope.page) {
                $scope.page = 1;
                $scope.query.offset = 0;
                query_api($scope.query);
            }

            // In case of no results, the number of pages is one.
            if ($scope.numpages == 0) {
                $scope.numpages = 1
            }
            ;
        });

        $scope.paginate_down = function () {
            if ($scope.page > 1) {
                $scope.page -= 1;
                $scope.query.offset = $scope.query.limit * ($scope.page - 1);
                query_api($scope.query);
            }
        }

        $scope.paginate_up = function () {
            if ($scope.numpages > $scope.page) {
                $scope.page += 1;
                $scope.query.offset = $scope.query.limit * ($scope.page - 1);
                query_api($scope.query);
            }
        }

        $scope.scroll_top = function () {
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }

        $scope.sync_pagination_scroll = function (up) {
            if (up) {
                const paginate = new Promise(function (resolve, reject) {
                    $scope.paginate_up()
                    resolve(true);
                });
                paginate.then((v) => {
                    $scope.scroll_top()
                })
            } else {
                const paginate = new Promise(function (resolve, reject) {
                    $scope.paginate_down()
                    resolve(true);
                });
                paginate.then((v) => {
                    $scope.scroll_top()
                })
            }

        }
        /*
        * End pagination
        */

        if (!Configs.hasOwnProperty("disableQuerySync")) {
            // Keep in sync the page location with the query object
            $scope.$watch('query', function () {
                $location.search($scope.query);
            }, true);
        }

        // Hierarchical keyword listeners
        $scope.$on('select_h_keyword', function ($event, element) {
            var data_filter = 'keywords__slug__in';
            var query_entry = [];
            var value = (element.href ? element.href : element.text);
            // If the query object has the record then grab it
            if ($scope.query.hasOwnProperty(data_filter)) {

                // When in the location are passed two filters of the same
                // type then they are put in an array otherwise is a single string
                if ($scope.query[data_filter] instanceof Array) {
                    query_entry = $scope.query[data_filter];
                } else {
                    query_entry.push($scope.query[data_filter]);
                }
            }

            // Add the entry in the correct query
            if (query_entry.indexOf(value) == -1) {
                query_entry.push(value);
            }

            //save back the new query entry to the scope query
            $scope.query[data_filter] = query_entry;

            query_api($scope.query);
        });

        $scope.$on('unselect_h_keyword', function ($event, element) {
            var data_filter = 'keywords__slug__in';
            var query_entry = [];
            var value = (element.href ? element.href : element.text);
            // If the query object has the record then grab it
            if ($scope.query.hasOwnProperty(data_filter)) {

                // When in the location are passed two filters of the same
                // type then they are put in an array otherwise is a single string
                if ($scope.query[data_filter] instanceof Array) {
                    query_entry = $scope.query[data_filter];
                } else {
                    query_entry.push($scope.query[data_filter]);
                }
            }

            query_entry.splice(query_entry.indexOf(value), 1);

            //save back the new query entry to the scope query
            $scope.query[data_filter] = query_entry;

            //if the entry is empty then delete the property from the query
            if (query_entry.length == 0) {
                delete ($scope.query[data_filter]);
            }
            query_api($scope.query);
        });

        /*
        * Add the selection behavior to the element, it adds/removes the 'active' class
        * and pushes/removes the value of the element from the query object
        */
        $scope.multiple_choice_listener = function ($event) {
            var element = $($event.currentTarget);
            var query_entry = [];
            var data_filter = element.attr('data-filter');
            var value = element.attr('data-value');

            // If the query object has the record then grab it
            if ($scope.query.hasOwnProperty(data_filter)) {

                // When in the location are passed two filters of the same
                // type then they are put in an array otherwise is a single string
                if ($scope.query[data_filter] instanceof Array) {
                    query_entry = $scope.query[data_filter];
                } else {
                    query_entry.push($scope.query[data_filter]);
                }
            }

            // If the element is active active then deactivate it
            if (element.hasClass('active')) {
                // clear the active class from it
                element.removeClass('active');

                // Remove the entry from the correct query in scope

                query_entry.splice(query_entry.indexOf(value), 1);
            }
            // if is not active then activate it
            else if (!element.hasClass('active')) {
                // Add the entry in the correct query
                if (query_entry.indexOf(value) == -1) {
                    query_entry.push(value);
                }
                element.addClass('active');
            }

            //save back the new query entry to the scope query
            $scope.query[data_filter] = query_entry;

            //if the entry is empty then delete the property from the query
            if (query_entry.length == 0) {
                delete ($scope.query[data_filter]);
            }
            query_api($scope.query);
        }

        $scope.single_choice_listener = function ($event) {
            var element = $($event.currentTarget);
            var query_entry = [];
            var data_filter = element.attr('data-filter');
            var value = element.attr('data-value');
            // Type of data being displayed, use 'content' instead of 'all'
            $scope.dataValue = (value == 'all') ? 'content' : value;

            // If the query object has the record then grab it
            if ($scope.query.hasOwnProperty(data_filter)) {
                query_entry = $scope.query[data_filter];
            }

            if (!element.hasClass('selected')) {
                // Add the entry in the correct query
                query_entry = value;

                // clear the active class from it
                element.parents('ul').find('a').removeClass('selected');

                element.addClass('selected');

                //save back the new query entry to the scope query
                $scope.query[data_filter] = query_entry;

                query_api($scope.query);
            }
        }

        $('#text_search_btn').click(function () {
            if (HAYSTACK_SEARCH) {
                $scope.query['q'] = $('#text_search_input').val();
            } else {
                if (AUTOCOMPLETE_URL_RESOURCEBASE == "/people/autocomplete/") { // updated url to work with new autocomplete backend format
                    // a user profile has no title; if search was triggered from
                    // the /people page, filter by username instead
                    var query_key = 'username__icontains';
                } else if (AUTOCOMPLETE_URL_RESOURCEBASE == "/groups/autocomplete_category/") {
                    // Adding in this conditional since both groups autocomplete and searches requests need to search name not title.
                    var query_key = 'name__icontains';
                } else if (AUTOCOMPLETE_URL_RESOURCEBASE == "/groups/autocomplete/") {
                    // Adding in this conditional since both groups autocomplete and searches requests need to search name not title.
                    var query_key = $('#text_search_input').data('query-key') || 'title';
                } else {
                    var query_key = $('#text_search_input').data('query-key') || 'title__icontains';
                }
                $scope.query[query_key] = $('#text_search_input').val();
            }
            $scope.query['abstract__icontains'] = $('#text_search_input').val();
            $scope.query['purpose__icontains'] = $('#text_search_input').val();
            $scope.query['f_method'] = 'or';
            query_api($scope.query);
        });

        $('#region_search_btn').click(function () {
            $scope.query['regions__name__in'] = $('#region_search_input').val();
            query_api($scope.query);
        });

        $scope.feature_select = function ($event) {
            var element = $(event.currentTarget);
            var article = $(element.parents('article')[0]);
            if (article.hasClass('resource_selected')) {
                element.html('Select');
                article.removeClass('resource_selected');
            } else {
                element.html('Deselect');
                article.addClass('resource_selected');
            }
        };

        /*
        * Date management
        */

        $scope.date_query = {
            'date__gte': '',
            'date__lte': ''
        };
        var init_date = true;
        $scope.$watch('date_query', function () {
            if ($scope.date_query.date__gte != '' && $scope.date_query.date__lte != '') {
                var dateGte = new Date($scope.date_query.date__gte).toISOString();
                var dateLte = new Date($scope.date_query.date__lte).toISOString();
                $scope.query['date__range'] = dateGte + ',' + dateLte;
                delete $scope.query['date__gte'];
                delete $scope.query['date__lte'];
            } else if ($scope.date_query.date__gte != '') {
                var dateGte = new Date($scope.date_query.date__gte).toISOString();
                $scope.query['date__gte'] = dateGte;
                delete $scope.query['date__range'];
                delete $scope.query['date__lte'];
            } else if ($scope.date_query.date__lte != '') {
                var dateLte = new Date($scope.date_query.date__lte).toISOString();
                $scope.query['date__lte'] = dateLte;
                delete $scope.query['date__range'];
                delete $scope.query['date__gte'];
            } else {
                delete $scope.query['date__range'];
                delete $scope.query['date__gte'];
                delete $scope.query['date__lte'];
            }
            if (!init_date) {
                query_api($scope.query);
            } else {
                init_date = false;
            }

        }, true);

        /*
         * Spatial search
         */
        if ($('.leaflet_map').length > 0) {
            angular.extend($scope, {
                layers: [
                    {
                        name: 'OpenStreetMap',
                        active: true,
                        source: {
                            type: 'OSM'
                        }
                    }
                ],
                center: {
                    lat: 0.0,
                    lon: 0.0,
                    zoom: 1
                },
                defaults: {
                    interactions: {
                        mouseWheelZoom: true
                    },
                    controls: {
                        zoom: {
                            position: 'topleft'
                        }
                    }
                }
            });

            var olData = $injector.get('olData'),
                map = olData.getMap('filter-map');

            map.then(function (map) {
                map.on('moveend', function () {
                    var glbox = map.getView().calculateExtent(map.getSize()); // doesn't look as expected.
                    var box = ol.proj.transformExtent(glbox, 'EPSG:3857', 'EPSG:4326');
                    $scope.query['extent'] = box.toString();
                    query_api($scope.query);
                });
            });

            var showMap = false;
            $('#_extent_filter').click(function (evt) {
                showMap = !showMap
                if (showMap) {
                    olData.getMap().then(function (map) {
                        map.updateSize();
                    });
                }
            });
        }
    });
})();