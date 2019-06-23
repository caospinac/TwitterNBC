import React, { Component } from 'react'
import { Container, Row, Col } from 'reactstrap';

import InputForm from './components/inputForm'
import DocumentDetail from './components/documentDetail'

import logo from './logo.svg';
import './App.css';
import Util from './util';

const util = new Util();
global.ajax = util.ajax;

export default class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            result: {},
            isLoading: false
        }
        this.onSubmit = this.onSubmit.bind(this);
    }

    async onSubmit(formData) {
        this.setState({
            isLoading: true
        })
        let response = await global.ajax({
            url: "/api/v1/nbc",
            params: {
                t: formData.text || ""
            }
        });
        this.setState({
            result: response.data,
            isLoading: false
        })

    }

    render() {
        const { result, isLoading } = this.state;
        return (
            <Container>
                <h1>Sentiment Analysis App</h1>
                <Row>
                    <Col>
                        <InputForm onSubmit={this.onSubmit} disabled={isLoading}></InputForm>
                    </Col>
                </Row>
                {result.data && <div>
                    <hr />
                    <Row>
                        <Col>
                            <DocumentDetail data={result.data}>
                            </DocumentDetail>
                        </Col>
                    </Row>
                </div>}
            </Container>
        )
    }
}
