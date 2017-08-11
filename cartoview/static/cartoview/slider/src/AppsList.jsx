import './app.css'

import React, { Component } from 'react'

import Img from 'react-image'
import Slider from 'react-slick'
import Spinner from 'react-spinkit'
import { render } from 'react-dom'

export default class AppsList extends Component {
    constructor( props ) {
        super( props )
        this.state = {
            apps: [ ],
            loading: true
        }
    }
    loadApps = ( ) => {
        const url = "/api/app"
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
    componentWillMount( ) {
        this.loadApps( )
    }
    render( ) {
        let { apps, loading } = this.state
        return (
            <div>
                <h3>Applications</h3>
                <hr />
                {apps.length > 0 && <ul className="list-group">
                    {apps.map((app, i) => {
                        return <a href="javascript:;"><li onClick={()=>window.location.replace(`/apps/appinstances/?app__title=${app.title}`)} key={i} className="list-group-item">
                            {app.title}
                            <span className="badge pull-right">{app.app_instance_count}</span></li></a>
                    })}
                </ul>}
                {loading && <Spinner name="line-scale" />}
                {!loading && apps.length == 0 && <small>No Apps installed</small>}
                <hr />
            </div>
        )
    }
}
render( <AppsList />, document.getElementById( "react-apps-list" ) )
