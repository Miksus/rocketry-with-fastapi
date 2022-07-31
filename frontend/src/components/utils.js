

const API = "http://localhost:8000";
const REFRESH = 1000;

async function queryApi(route, method="GET") {
    console.log(`Querying ${API + route}`)
    let data = await fetch(
        API + route,
        {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json',
            }
        }
    ).then(response => {
        return response.json()
    });
    console.log(data)
    return data
}

function getVariant(status) {
    return {
        success: "success", run: "warning", fail: "danger", null: "dark"
    }[status]
}

function getStatus(status) {
    // Turn status more readable
    return {
        success: "Success", 
        run: "Running", 
        fail: "Failed", 
        null: "Not run", 
        terminate: "Terminated",
        crash: "Crashed",
        inaction: "Did nothing"
    }[status]
}

export { REFRESH, queryApi, getVariant, getStatus };