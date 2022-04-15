import React from "react";
import clsx from "clsx";
import styles from "./HomepageFeatures.module.css";
import Link from "@docusaurus/Link";

const FeatureList = [
  {
    title: "Windows 11 theming",
    Svg: require("../../static/img/icons8-windows-11.svg").default,
    description: (
      <>
        Uses{" "}
        <Link to="https://github.com/rdbende/Sun-Valley-TTk-Theme">
          {" "}
          Fluent Design Themeing
        </Link>
        and Mica, feels modern!
      </>
    ),
  },
  {
    title: "Built on Python",
    Svg: require("../../static/img/icons8-python.svg").default,
    description: (
      <>TimerX is built on top of Python and uses Tkinter TTk for the GUI.</>
    ),
  },
  {
    title: "Open-source",
    Svg: require("../../static/img/icons8-open-source.svg").default,
    description: (
      <>
        TimerX is open-source, meaning the code is available for everyone to see{" "}
        <i>and</i> modify at the{" "}
        <Link to="https://github.com/Futura-Py/TimerX">GitHub repo</Link>.
      </>
    ),
  },
];

function Feature({ Svg, title, description }) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        <Svg className={styles.featureSvg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
