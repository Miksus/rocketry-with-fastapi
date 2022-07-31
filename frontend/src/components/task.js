
import React, { useState } from 'react';

import { Alert, Col, Row, Container, Dropdown, Form, Button, Table, Tabs, Tab, Accordion, InputGroup, Badge, Card, Collapse, Navbar, Nav } from 'react-bootstrap';
import { Routes, Route, BrowserRouter, useParams, Link } from 'react-router-dom';

import { REFRESH, queryApi, getVariant, getStatus } from './utils.js'

class TaskPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            tasks: []
        }
        this.updateTasks.bind(this)
        //this.updateTasks()
    }

    async updateTasks() {
        let data = await queryApi("/tasks")
        this.setState({
            tasks: data
        })
    }

    componentDidMount() {
        this.updateTasks()
        this.interval = setInterval(() => this.updateTasks(), REFRESH);
        //this.interval_logs = setInterval(() => this.updateLogs(), 5000);
    }
    componentWillUnmount() {
        clearInterval(this.interval);
        //clearInterval(this.interval_logs);
    }

    render() {
        //this.updateTasks()
        console.log("Task!")
        console.log(this.props)
        return (
            <div>
                <Row>
                    <Col>
                        <TaskMenu tasks={this.state.tasks}/>
                    </Col>
                    <Col md="auto">
                        <Routes>
                            <Route path="/:id" element={
                                <TaskBox tasks={this.state.tasks}/>
                            } />
                        </Routes>
                    </Col>
                </Row>
            </div>
        )
    }
}

function TaskBox(props) {
    let { id } = useParams();

    let task = props.tasks.filter(task => task.name == id)[0];

    if (typeof task == 'undefined') {
        return <div></div>
    }
    return (
        <div>
            <TaskSummary task={ task }/>
        </div>
    )
}

class TaskMenu extends React.Component {
    constructor(props) {
        super(props);
    }

    renderTask(task, index) {
        const variant = getVariant(task.status);
        return (
            <tr key={index}>
                <th>
                    <Link to={`/tasks/${task.name}`}>
                        <Button variant={"outline-dark"} className="select-task">{task.name}</Button>
                    </Link>
                </th>
                <td>{getStatus(task.status)}</td>
            </tr>
        )
    }

    render() {
        console.log("Live")
        console.log(this.props.tasks)
        return (
            <Table>
                <thead>
                    <tr>
                        <th>Task name</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {this.props.tasks.map(this.renderTask.bind(this))}
                </tbody>
            </Table>
        )
    }
}


class TaskSummary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            task: props.task
        }
        this.commandTask.bind(this)
        this.getDisableEnableButton.bind(this)
    }

    run() {
        this.commandTask("run")
    }

    disable() {
        this.commandTask("disable")
    }

    enable() {
        this.commandTask("enable")
    }

    terminate() {
        this.commandTask("terminate")
    }

    commandTask(cmd) {
        let task = this.props.task; 
        queryApi(`/tasks/${task.name}/${cmd}`, "POST")
    }

    getDisableEnableButton(task) {
        const class_name = "btn-control"; 
        if (!task.disabled) {
            return <Button variant="danger" onClick={this.disable.bind(this)} className={class_name}>Disable</Button>
        } else {
            return <Button variant="danger" onClick={this.enable.bind(this)} className={class_name}>Enable</Button>
        }
    }

    render() {
        const task = this.props.task;
        
        //let { task_name } = this.props.match.params;

        console.log("Task Summary")
        //console.log(this.props.match.params)
        console.log(task)
        const border = getVariant(task.status);


        return (
            <div>
            <Card className={"task-summary border-" + border}>
                <Card.Header>{ task.name }</Card.Header>
                <Card.Body>
                    <Row>
                        <Col>
                            <Table>
                                <tbody>
                                    <tr>
                                        <th>Status</th>
                                        <td>{getStatus(task.status)}</td>
                                    </tr>
                                    <tr>
                                        <th>Last Run</th>
                                        <td>{task.last_run}</td>
                                    </tr>
                                    <tr>
                                        <th>Last Success</th>
                                        <td>{task.last_success}</td>
                                    </tr>
                                    <tr>
                                        <th>Last Failure</th>
                                        <td>{task.last_fail}</td>
                                    </tr>
                                    <tr>
                                        <th>Last Termination</th>
                                        <td>{task.last_terminate}</td>
                                    </tr>
                                </tbody>
                            </Table>
                            <div className="side-by-side-even">
                                <Button variant="success" onClick={this.run.bind(this)} className="btn-control">Run</Button>
                                {this.getDisableEnableButton(task)}
                                <Button variant="warning" onClick={this.terminate.bind(this)} className="btn-control" disabled={!task.is_running}>Terminate</Button>
                            </div>
                        </Col>
                        <Col>
                            <Form>
                                <fieldset disabled>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Description</Form.Label>
                                        <Form.Control value={task.description}/>
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label>Start Condition</Form.Label>
                                        <Form.Control value={task.start_cond}/>
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label>End Condition</Form.Label>
                                        <Form.Control value={task.end_cond} />
                                    </Form.Group>
                                    <div className="side-by-side">
                                        <Form.Group className="mb-3">
                                            <Form.Label>Priority</Form.Label>
                                            <Form.Control value={task.priority} />
                                        </Form.Group>
                                        <Form.Group className="mb-3">
                                            <Form.Label>Timeout</Form.Label>
                                            <Form.Control value={task.timeout} />
                                        </Form.Group>
                                    </div>
                                    <Button type="submit">Update</Button>
                                </fieldset>
                            </Form>
                        </Col>
                    </Row>
                </Card.Body>
            </Card>
            </div>
        )
    }
}

export default TaskPage;