import React, { Component } from 'react'
import { InputGroup, InputGroupAddon, Button, Input } from 'reactstrap';

export default class InputForm extends Component {

    constructor(props) {
        super(props);
        this.state = {
            text: ""
        }

        this.onChangeText = this.onChangeText.bind(this);
        this.onKeyUp = this.onKeyUp.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChangeText(e) {
        this.setState({
            text: e.target.value
        });
    }

    onKeyUp(e) {
        if (e.keyCode === 13) {
            this.onSubmit();
        }
    }

    onSubmit() {
        const { onSubmit } = this.props;
        onSubmit && onSubmit(this.state);
    }

    render() {
        const { disabled } = this.props;
        return (
            <InputGroup>
                <Input onChange={this.onChangeText} onKeyUp={this.onKeyUp} placeholder="Text" disabled={disabled}/>
                <InputGroupAddon addonType="append">
                    <Button onClick={this.onSubmit} disabled={disabled}>Analyze</Button>
                </InputGroupAddon>
            </InputGroup>
        )
    }
}
