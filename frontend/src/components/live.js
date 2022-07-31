
import React, { useState } from 'react';

import { Alert, Col, Row, Container, Dropdown, Form, Button, Table, Tabs, Tab, Accordion, InputGroup, Badge, Card, Collapse, Navbar, Nav } from 'react-bootstrap';
import { Routes, Route, BrowserRouter, useParams, Link } from 'react-router-dom';

import { REFRESH, queryApi, getVariant, getStatus } from './utils.js'

class LivePage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            tasks: [],
            logs: []
        }
        this.updateTasks.bind(this)
        //this.updateTasks()
    }

    render() {
        return (
            <div>
                <Row>
                    <Col>
                        <RunningTasksBox tasks={this.state.tasks}/>
                    </Col>
                    <Col>
                        <LiveLogs logs={this.state.logs}/>
                    </Col>
                </Row>
            </div>
        )
    }

    async updateTasks() {
        let data = await queryApi("/tasks")
        this.setState({
            tasks: data
        })

        await this.updateLogs()
    }

    async updateLogs() {
        let data = await queryApi("/logs?limit=5")
        this.setState({
            logs: data
        })
    }


    componentDidMount() {
        console.log("Mounted!")
        this.updateTasks()
        this.interval = setInterval(() => this.updateTasks(), REFRESH);
        //this.interval_logs = setInterval(() => this.updateLogs(), 5000);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
        //clearInterval(this.interval_logs);
    }
}

class RunningTasksBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            running_tasks: []
        }
        this.terminateTask.bind(this)
        //this.renderTask.bind(this)
    }

    terminateTask(task_name) {
        console.log("Terminating")
        queryApi(`/tasks/${task_name}/terminate`, "POST")

    }

    renderTask(task, index) {
        return (
            <div key={ index } className="RunningTasks">
                <Link to={`/tasks/${task.name}`} className="RunningTask">
                    <Alert variant="warning" className="RunningTask">{task.name}</Alert>
                </Link>
                <Button type="submit" variant="danger" onClick={this.terminateTask.bind(this, task.name)}>Terminate</Button>
            </div>
        )
    }

    getRunning() {
        // Get currently running tasks
        return this.props.tasks.filter(task => task.is_running)
    }

    render() {
        console.log("RunningTasksBox")
        console.log(this.props.tasks)
        let running_tasks = this.getRunning()
        return (
            <div>
                <h2>Running tasks</h2>
                {running_tasks.map(this.renderTask.bind(this))}
            </div>
        )
    }
}

class LiveLogs extends React.Component {
    constructor(props) {
        super(props);
        this.renderHeaders.bind(this)
    }

    renderHeaders(headers) {

        return (
            <thead>
                <tr>
                    <th>#</th>
                    {headers.map(function(name, index) {
                        return <th key={index}>{ name }</th>
                    })}

                </tr>
            </thead>
        )
    }

    renderRow(headers, log, index) {
        //const headers = this.state.headers;¨

        return (
            <tr>
            <td key={index}>{ index }</td>
            {headers.map(function(field, index) {
                return <td key={index}>{ log[field] }</td>
            })}
            </tr>
        )
    }

    renderBody(headers) {
        return (
            <tbody>
                    {this.props.logs.map(this.renderRow.bind(this, headers))}
            </tbody>
        )
    }

    render() {
        console.log(this.props.logs)
        const headers = Object.keys(this.props.logs.length != 0 ? this.props.logs[0]: {});
        return (
            <div>
                <h2>Live Logs</h2>
                <Table striped bordered hover variant="dark">
                    {this.renderHeaders(headers)}
                    {this.renderBody(headers)}
                </Table>
            </div>
        )
    }
}

export default LivePage;