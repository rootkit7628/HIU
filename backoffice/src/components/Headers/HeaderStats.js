import React from "react";

// components

import CardStats from "components/Cards/CardStats.js";
import "../../assets/styles/cardStyle.css"

export default function HeaderStats() {
  return (
    <>
      {/* Header */}
      <div className="relative  md:pt-32 pb-32 pt-12" style={{backgroundColor: "rgba(36, 114, 205, 1)"}}>
        <div className="px-4 md:px-10 w-full header-stat" >
          <div>
            {/* Card stats */}
            <div className="flex flex-wrap">
              <div className="w-full lg:w-6/12 xl:w-3/12 px-4">
                <CardStats
                  statSubtitle="Fichiers"
                  statTitle="2"
                  statArrow="up"
                  statPercent=""
                  statPercentColor="text-emerald-500"
                  statDescripiron="Since last week"
                  statIconName="far fa-chart-bar"
                  statIconColor="bg-red-500"
                />
              </div>
              <div className="w-full lg:w-6/12 xl:w-3/12 px-4">
                <CardStats
                  statSubtitle="Download"
                  statTitle="49"
                  statArrow="up"
                  statPercent="12"
                  statPercentColor="text-emerald-500"
                  statDescripiron="Since yeasterday"
                  statIconName="fas fa-percent"
                  statIconColor="bg-lightBlue-500"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
