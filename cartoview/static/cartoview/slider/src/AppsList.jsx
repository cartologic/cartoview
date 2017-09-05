import './app.css'

import React, { Component } from 'react'

import Equalizer from 'react-equalizer'
import Spinner from 'react-spinkit'
import { render } from 'react-dom'

export default class AppsList extends Component {
    constructor(props) {
        super(props)
        this.state = {
            apps: [],
            tools: [],
            loading: true
        }
    }
    loadApps = () => {
        const url = "/api/app/?single_instance=false"
        fetch(url).then((response) => response.json()).then((data) => {
            this.setState({
                apps: data.objects.sort((a, b) => {
                    if (a.order < b.order) {
                        return -1
                    }
                    if (a.order > b.order) {
                        return 1
                    }
                }),
                loading: false
            })
        })
    }
    loadTools = () => {
        const url = "/api/app/?single_instance=true"
        fetch(url).then((response) => response.json()).then((data) => {
            this.setState({
                tools: data.objects.sort((a, b) => {
                    if (a.order < b.order) {
                        return -1
                    }
                    if (a.order > b.order) {
                        return 1
                    }
                }),
                loading: false
            })
        })
    }
    componentWillMount() {
        this.loadApps()
        this.loadTools()
    }
    render() {
        let { apps, loading, tools } = this.state
        return (
            <div>

                {apps.length > 0 && <div className="panel-group">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            <h4 className="panel-title">
                                <a data-toggle="collapse" href="#collapse1">Applications</a>
                            </h4>
                        </div>
                        <div id="collapse1" className="panel-collapse collapse in">
                            <ul className="list-group">
                                {apps.map((app, i) => {
                                    return <a key={i} href="javascript:;"><li onClick={() => window.location.replace(`/apps/appinstances/?app__title=${app.title}`)} key={i} className="list-group-item">
                                        {app.title}
                                        <span className="badge pull-right">{app.app_instance_count}</span></li></a>
                                })}
                            </ul>
                        </div>
                    </div>
                </div>}

                {loading && <Spinner name="line-scale" />}
                {!loading && apps.length == 0 && <small>No Apps installed</small>}
                <hr />

                {tools.length > 0 && <div className="panel-group">
                    <div className="panel panel-default">
                        <div className="panel-heading">
                            <h4 className="panel-title">
                                <a data-toggle="collapse" href="#collapse2">Tools</a>
                            </h4>
                        </div>
                        <div  id="collapse2" className="panel-collapse collapse in">
                            <Equalizer byRow={false} property="height">
                                {tools.map((tool, i) => {
                                    return <div key={i} className="col-xs-6 col-sm-6 col-md-6 col-lg-6 text-center"><a href="javascript:;" onClick={() => window.location.replace(`/apps/${tool.name}/`)}>
                                        <img className="img-responsive img-circle" src={`/static/${tool.name}/logo.png`} />
                                        <p style={{ wordBreak: "normal", textAlign: 'center' }}>{tool.title}</p>
                                    </a>
                                    </div>

                                })}

                            </Equalizer>
                        </div>
                    </div>
                </div>}
                {loading && <Spinner name="line-scale" />}
                {!loading && tools.length == 0 && <small>No Tools installed</small>}
                <hr />
            </div>
        )
    }
}
render(<AppsList />, document.getElementById("react-apps-list"))
