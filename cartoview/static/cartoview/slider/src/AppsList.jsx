import './app.css'

import React, { Component } from 'react'

import Spinner from 'react-spinkit'
import { render } from 'react-dom'

export default class AppsList extends Component {
    constructor( props ) {
        super( props )
        this.state = {
            apps: [ ],
            tools:[],
            loading: true
        }
    }
    loadApps = ( ) => {
        const url = "/api/app/?single_instance=false"
        fetch( url ).then( ( response ) => response.json( ) ).then( ( data ) => {
            this.setState( {
                apps: data.objects.sort( ( a, b ) => {
                    if ( a.order < b.order ) {
                        return -1
                    }
                    if ( a.order > b.order ) {
                        return 1
                    }
                } ),
                loading: false
            } )
        } )
    }
    loadTools = ( ) => {
        const url = "/api/app/?single_instance=true"
        fetch( url ).then( ( response ) => response.json( ) ).then( ( data ) => {
            this.setState( {
                tools: data.objects.sort( ( a, b ) => {
                    if ( a.order < b.order ) {
                        return -1
                    }
                    if ( a.order > b.order ) {
                        return 1
                    }
                } ),
                loading: false
            } )
        } )
    }
    componentWillMount( ) {
        this.loadApps( )
        this.loadTools()
    }
    render( ) {
        let { apps, loading,tools } = this.state
        return (
            <div>
                <h3>Applications</h3>
                <hr />
                {apps.length > 0 && <ul className="list-group">
                    {apps.map((app, i) => {
                        return <a key={i} href="javascript:;"><li  onClick={()=>window.location.replace(`/apps/appinstances/?app__title=${app.title}`)} key={i} className="list-group-item">
                            {app.title}
                            <span className="badge pull-right">{app.app_instance_count}</span></li></a>
                    })}
                </ul>}
                {loading && <Spinner name="line-scale" />}
                {!loading && apps.length == 0 && <small>No Apps installed</small>}
                <hr />
                <h3>Tools</h3>
                <hr />
                {tools.length > 0 && <ul className="list-group">
                    {tools.map((tool, i) => {
                        return <a key={i} href="javascript:;"><li  onClick={()=>window.location.replace(`/apps/${tool.name}/`)} key={i} className="list-group-item">
                            {tool.title}</li></a>
                    })}
                </ul>}
                {loading && <Spinner name="line-scale" />}
                {!loading && tools.length == 0 && <small>No Tools installed</small>}
                <hr />
            </div>
        )
    }
}
render( <AppsList />, document.getElementById( "react-apps-list" ) )
