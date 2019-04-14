import React, { useContext } from 'react'

import { BasicViewerContext } from '../context'
import CircularProgress from '@material-ui/core/CircularProgress'
import LinearProgress from '@material-ui/core/LinearProgress'
import PropTypes from 'prop-types'
import Snackbar from '@material-ui/core/Snackbar'
import Typography from '@material-ui/core/Typography'

export const Loader = (props) => {
    const { size, thickness, align, type } = props
    return (
        <div className={`text-${align || "center"}`} >
            {(typeof (type) === "undefined" || type === "circle") && <CircularProgress size={size ? size : 50} thickness={thickness ? thickness : 5} className="text-center"></CircularProgress>}
            {type === "line" && <LinearProgress size={size ? size : 50} thickness={thickness ? thickness : 5} className="text-center"></LinearProgress>}
        </div>
    )
}
Loader.propTypes = {
    size: PropTypes.number,
    thickness: PropTypes.number,
    align: PropTypes.string,
    type: PropTypes.string
}
export const Message = (props) => {
    const { align, type, message, color, noWrap } = props
    return <Typography variant={type} align={align ? align : "center"} noWrap={typeof (noWrap) !== "undefined" ? noWrap : message.length > 70 ? true : false} color={color ? color : "inherit"} className="element-flex">{message}</Typography>
}
Message.propTypes = {
    type: PropTypes.string.isRequired,
    message: PropTypes.string.isRequired,
    align: PropTypes.string,
    color: PropTypes.string,
    noWrap: PropTypes.bool,
}
const SnackMessage = (props) => {
    const { message } = props
    return <span className="element-flex" id="message-id"><Loader size={20} thickness={4} /> {message} </span>
}
SnackMessage.propTypes = {
    message: PropTypes.string.isRequired
}
export const CartoviewSnackBar = (props) => {
    const { featureIdentifyLoading } = useContext(BasicViewerContext)
    const messageComponent = <SnackMessage message={"Searching For Features at this Point"} />
    return <Snackbar
        open={featureIdentifyLoading}
        ContentProps={{
            'aria-describedby': 'message-id',
        }}
        message={messageComponent} />
}