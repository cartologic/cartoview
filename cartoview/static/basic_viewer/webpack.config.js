module.exports = ( env, argv ) => {
    const CleanWebpackPlugin = require( 'clean-webpack-plugin' )
    const MiniCssExtractPlugin = require( "mini-css-extract-plugin" )
    const OptimizeCSSAssetsPlugin = require(
        "optimize-css-assets-webpack-plugin" )
    var webpack = require( 'webpack' )
    const UglifyJsPlugin = require( 'uglifyjs-webpack-plugin' )
    const BundleAnalyzerPlugin = require( 'webpack-bundle-analyzer' ).BundleAnalyzerPlugin
    var path = require( 'path' )
    const CaseSensitivePathsPlugin = require(
        'case-sensitive-paths-webpack-plugin' )
    const APP_DIR = path.resolve( __dirname, 'src' )
    const production = argv.mode === 'production'
    var filename = !production ? '[name].bundle.js' :
        '[name].[hash].bundle.js'
    const autoprefixer = require( 'autoprefixer' )
    const plugins = [
        new webpack.DefinePlugin( {
            'process.env': {
                'NODE_ENV': JSON.stringify( production ?
                    'production' : '' )
            },
        } ),
        new CaseSensitivePathsPlugin(),
        new CleanWebpackPlugin( [ 'dist' ] ),
        new MiniCssExtractPlugin( {
            filename: !production ? '[name].css' : '[name].[hash].css',
            chunkFilename: !production ? '[id].css' : '[id].[hash].css',
        } ),

    ]
    const config = {
        mode: production ? "production" : "development",
        context: path.resolve( __dirname ),
        entry: {
            extVendors: [ 'react-redux', 'redux', ],
            polyfill: [ '@babel/polyfill', ],
            react: [ 'react', 'react-dom' ],
            materialUI: [ '@material-ui/core', ],
            lodashLib: [ 'lodash', ],
            basicViewer: [ path.join( APP_DIR, 'containers',
                'basicViewer.jsx' ), ],
        },
        output: {
            path: path.resolve( __dirname, './dist' ),
            filename: filename,
            chunkFilename: '[name].js',
            publicPath: '/static/basic_viewer/dist/',
        },
        optimization: {
            splitChunks: {
                chunks: 'all',
                minSize: 1000,
                minChunks: 2,
                maxAsyncRequests: 5,
                maxInitialRequests: 3,
                name: true,
                cacheGroups: {
                    default: {
                        minChunks: 1,
                        priority: -20,
                        reuseExistingChunk: true,
                    },
                    extVendors: {
                        chunks: 'all',
                        name: 'extVendors',
                        test: 'extVendors',
                        enforce: true
                    },
                    react: {
                        chunks: 'all',
                        name: 'react',
                        test: 'react',
                        enforce: true
                    },
                    materialUI: {
                        chunks: 'all',
                        name: 'materialUI',
                        test: 'materialUI',
                        enforce: true
                    },
                    lodashLib: {
                        chunks: 'all',
                        name: 'lodashLib',
                        test: 'lodashLib',
                        enforce: true
                    },
                    polyfill: {
                        chunks: 'all',
                        name: 'polyfill',
                        test: 'polyfill',
                        enforce: true
                    },
                    vendors: {
                        test: /[\\/]node_modules[\\/]/,
                        priority: -10,
                    }
                },
            }
        },
        node: {
            fs: "empty"
        },
        plugins: plugins,
        resolve: {
            extensions: [ '*', '.js', '.jsx' ],
            alias: {
                Source: APP_DIR
            },
        },
        module: {
            rules: [ {
                    test: /\.(js|jsx)$/,
                    loader: 'babel-loader',
            },
                {
                    test: /\.css$/,
                    use: [
                    require.resolve( 'style-loader' ),
                    MiniCssExtractPlugin.loader,
                        {
                            loader: require.resolve(
                                'css-loader' ),
                            options: {
                                importLoaders: 1,
                            },
                    },
                        {
                            loader: require.resolve(
                                'postcss-loader' ),
                            options: {
                                // Necessary for external CSS imports to work
                                // https://github.com/facebookincubator/create-react-app/issues/2677
                                ident: 'postcss',
                                plugins: () => [
                                require( 'postcss-flexbugs-fixes' ),
                                autoprefixer( {
                                        browsers: [
                                        '>1%',
                                        'last 4 versions',
                                        'Firefox ESR',
                                        'not ie < 9', // React doesn't support IE8 anyway
                                    ],
                                        flexbox: 'no-2009',
                                    } ),
                            ],
                            },
                    },
                ],
            },
                {
                    test: /\.xml$/,
                    loader: 'raw-loader'
            },
                {
                    test: /\.html$/,
                    use: [ 'html-loader' ]
            },
                {
                    type: 'javascript/auto',
                    test: /\.json$/,
                    use: [
                        {
                            loader: 'json-loader'
                    }
                ]
            },
                {
                    test: /\.(woff|woff2|eot|ttf|otf|jpg|png|gif|svg)$/,
                    use: [ 'file-loader' ]
            }
            ],
            noParse: [ /dist\/ol\.js/, /dist\/jspdf.debug\.js/,
                /dist\/js\/tether\.js/
            ]
        }
    }
    if ( production ) {
        const prodPlugins = [
            new webpack.NoEmitOnErrorsPlugin(),
            new webpack.optimize.ModuleConcatenationPlugin(),
            new webpack.HashedModuleIdsPlugin(),
            new BundleAnalyzerPlugin()
        ]
        Array.prototype.push.apply( plugins, prodPlugins )
        config.optimization.minimize = true
        config.optimization.minimizer = [
            new UglifyJsPlugin( {
                uglifyOptions: {
                    compress: {
                        warnings: false,
                        pure_getters: true,
                        unsafe: true,
                        unsafe_comps: true,
                    },
                    output: {
                        comments: false,
                    }
                },
                exclude: [ /\.min\.js$/gi ],
                sourceMap: true
            } ),
            new OptimizeCSSAssetsPlugin( {} )
        ]
    } else {
        const devPlugin = [
        ]
        config.devtool = 'cheap-module-source-map'
        Array.prototype.push.apply( plugins, devPlugin )
    }
    return config
}
