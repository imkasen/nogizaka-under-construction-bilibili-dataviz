"use strict";

import {drawChart} from "./container.js";
import {drawChart2} from "./container2.js";

let urls = [
    'resources/bv_info.json',
    'resources/bv_info2.json',
];

async function fetchURLs() {
    try {
        return await Promise.allSettled(
            urls.map(
                (url) => fetch(url)
                    .then((res) => res.json())
            )
        );
        // return await Promise.all([
        //     fetch('resources/bv_info.json')
        //         .then((res) => res.json()),
        //     fetch('resources/bv_info2.json')
        //         .then((res) => res.json()),
        // ]);
    } catch (error) {
        console.log(error);
    }
}

fetchURLs().then((data) => {
    // Promise.all
    // drawChart(data[0]);
    // drawChart2(data[1]);

    // Promise.allSettled
    if (data[0].status === "fulfilled") {
        drawChart(data[0].value);
    } else {
        // rejected
        console.log(data[0].reason);
    }
    if (data[1].status === "fulfilled") {
        drawChart2(data[1].value);
    } else {
        // rejected
        console.log(data[1].reason);
    }
});
