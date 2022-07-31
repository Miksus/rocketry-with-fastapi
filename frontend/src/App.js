import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

import { Alert, Col, Row, Container, Dropdown, Form, Button, Table, Tabs, Tab, Accordion, InputGroup, Badge, Card, Collapse, Navbar, Nav, Carousel } from 'react-bootstrap';
import { Routes, Route, BrowserRouter, useParams, Link } from 'react-router-dom';

import LivePage from './components/live.js';
import TaskPage from './components/task.js';

class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const logs = [
            {name: "do_stuff", runtime: "2 sec"},
        ];
        return (
            <div className="App">
                <Navbar bg="dark" variant="dark">
                    <Container>
                        <Navbar.Brand href="/">Rocketry</Navbar.Brand>
                        <Nav className="me-auto">
                            <Nav.Link href="/live">Live</Nav.Link>
                            <Nav.Link href="/tasks">Tasks</Nav.Link>
                            <Nav.Link href="/session">Session</Nav.Link>
                        </Nav>
                    </Container>
                </Navbar>
                <BrowserRouter>
                    <Routes>
                    <Route exact path="/" element={
                            <AboutPage/>
                        }/>
                        <Route exact path="/live" element={
                            <LivePage/>
                        }/>
                        <Route exact path="/tasks/*" element={
                            <TaskPage/>
                        }/>
                    </Routes>
                </BrowserRouter>
            </div>
        )
    }
}


class AboutPage extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        return (
            <div>
                <h2>Built with:</h2>
                <Carousel variant="dark">
                    <Carousel.Item interval={5000000}>
                        <img
                        className="d-block w-100 demo-logo"
                        src={require('./imgs/rocketry.png')}
                        alt="First slide"
                        />
                        <Carousel.Caption>
                            <h3><a href="https://rocketry.readthedocs.io/">Rocketry</a></h3>
                            <p>
                                Rocketry is used as the scheduler. Rocketry is a modern automation
                                back-end with a condition mechanism for scheduling.
                            </p>

                        </Carousel.Caption>
                    </Carousel.Item>
                    <Carousel.Item interval={5000}>
                    <img
                        className="d-block w-100 demo-logo"
                        src={require('./imgs/fastapi.png')}
                        alt="First slide"
                        />

                        <Carousel.Caption>
                            <h3><a href="https://fastapi.tiangolo.com">FastAPI</a></h3>
                            <p>
                                FastAPI is used as the REST API to communicate with the scheduler.
                                FastAPI is a modern web framework for APIs.
                            </p>
                        </Carousel.Caption>
                    </Carousel.Item>
                    <Carousel.Item interval={5000}>
                    <img
                        className="d-block w-100 demo-logo"
                        src={require('./imgs/react.png')}
                        alt="First slide"
                        />

                        <Carousel.Caption>
                        <h3><a href="https://reactjs.org">React</a></h3>
                            <p>
                                React is used as the graphical interface. React is a Javascript
                                library for interactive user interfaces.
                            </p>
                        </Carousel.Caption>
                    </Carousel.Item>
                </Carousel>
                <p>
                    Author: <a href="https://github.com/Miksus">Mikael Koli</a>
                </p>
            </div>
        )
    }
}

export default App;
