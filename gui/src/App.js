import React, { Component } from 'react'
import { Button, Container, InputGroup, InputGroupAddon, Input, Row, Col, Spinner } from 'reactstrap';

import InputForm from './components/inputForm'
import DocumentDetail from './components/documentDetail'

// import logo from './logo.svg';
import './App.css';
import Util from './util';

const util = new Util();
global.ajax = util.ajax;
global.openFile = util.openFile;
global.readFile = util.readFile;

export default class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            result: {},
            tweets: [],
            textSearch: "",
            isLoading: false
        }
        this.onSubmit = this.onSubmit.bind(this);
        this.onChangeTextSearch = this.onChangeTextSearch.bind(this);
        this.onKeyUpSearch = this.onKeyUpSearch.bind(this);
        this.onSubmitSearch = this.onSubmitSearch.bind(this);
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

    onChangeTextSearch(e) {
        this.setState({
            textSearch: e.target.value
        });
    }

    onKeyUpSearch(e) {
        if (e.keyCode === 13) {
            this.onSubmitSearch();
        }
    }

    async onSubmitSearch() {
        const { textSearch } = this.state;
        if (!textSearch) {
            return;
        }
        this.setState({
            isLoading: true
        })
        let response = await global.ajax({
            url: "/api/v1/twitter/search",
            params: {
                q: textSearch,
                classify: true
            }
        });
        this.setState({
            tweets: response.data.data || [],
            isLoading: false
        })
    }

    render() {
        const { result, tweets, textSearch, isLoading } = this.state;
        return (
            <Container>
                <h1>Sentiment Analysis App {isLoading && <Spinner style={{ width: '3rem', height: '3rem' }} type="grow" />}</h1>
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
                <hr />
                <Row>
                    <Col>
                        <InputGroup>
                            <InputGroupAddon addonType="prepend">Tweet search</InputGroupAddon>
                            <Input value={textSearch} onKeyUp={this.onKeyUpSearch}
                                    readOnly={isLoading} onChange={this.onChangeTextSearch} placeholder="" />
                            <InputGroupAddon addonType="append">
                                <Button onClick={this.onSubmitSearch} disabled={isLoading}>Search</Button>
                            </InputGroupAddon>
                        </InputGroup>
                        <div>
                            <small className="light-text" style={{marginRight: "5px"}}>
                                <i className="">Enter to search</i>
                            </small>
                        </div>
                        {tweets.length > 0 && tweets.map((tweet, index) => {
                            return (
                                <div key={index}>
                                    <DocumentDetail data={tweet.nbc}>
                                        <a href={"https://twitter.com/user/status/" + tweet._id}
                                                target="_blank">
                                            Go to tweet
                                        </a>
                                    </DocumentDetail>
                                </div>
                            )
                        })

                        }
                    </Col>
                </Row>
            </Container>
        )
    }
}
