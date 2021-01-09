"use strict";

import {drawChart} from "./container.js";
import {drawChart2} from "./container2.js";

async function fetchURLs() {
  try {
    return await Promise.all([
      fetch('resources/bv_info.json')
          .then((res) => res.json()),
      fetch('resources/bv_info2.json')
          .then((res) => res.json()),
    ]);
  } catch (error) {
    console.log(error);
  }
}

fetchURLs().then((data) => {
  drawChart(data[0]);
  drawChart2(data[1]);
});
