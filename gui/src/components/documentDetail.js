import React, { Component } from 'react'
import { Alert, Badge } from 'reactstrap';

export default class DocumentDetail extends Component {

    constructor(props) {
        super(props);
        this.state = {
            data: props.data
        }

        this.getType = this.getType.bind(this);
    }

    componentWillReceiveProps(props) {
        this.setState({
            data: props.data
        })
    }

    getType(data) {
        let color, text;
        switch(data.trend) {
            case "pos":
                color = "success";
                text = "Positive"
                break;
            case "neg":
                color = "danger";
                text = "Negative"
                break;
            default:
                color = null;
                text = "";
        }
        return (
            <Badge color={color}>{text}</Badge>
        )
    }

    render() {
        const { data } = this.state;
        const { pos, neg } = data;
        return (
            <div className="spaced">
                {data && (
                    <Alert color="dark">
                        <span>
                            {data.document}
                        </span>
                        <br></br>
                        <span>
                            {this.getType(data)}
                        </span>
                        <span>
                            {this.props.children}
                        </span>
                        <small className="light-text pull-right">
                            <i className="">Positive: {(pos * 100).toFixed(2)}%</i>
                            <i className="">Negative: {(neg * 100).toFixed(2)}%</i>
                        </small>
                    </Alert>
                )}
            </div>
        )
    }
}
