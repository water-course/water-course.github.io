/* Global video lists and embed helpers for the Water Course MkDocs site. */

window.waterCycleVideos = [
  {
    id: "R-9kn8gOdps",
    title: "What is hydrology?",
    label: "Water Cycle · Short video",
    description: "See why hydrology focuses on fresh water and where that small share of Earth’s water occurs. The video connects water science with irrigation, reservoirs, and water supply."
  },
  {
    id: "1Rn-u_JCPmY",
    title: "Why water behaves differently",
    label: "Water Cycle · Short video",
    description: "Learn how density, specific heat capacity, and latent heat make water unusual. These properties keep lakes habitable, moderate climate, and move energy through the atmosphere."
  },
  {
    id: "re7VP-KYxxQ",
    title: "Catchment delineation",
    label: "Water Cycle · Short video",
    description: "Follow contour lines and ridges to draw the land area that drains to one outlet. The video introduces drainage divides and the logic behind digital elevation models."
  },
  {
    id: "LKgIXug8Lac",
    title: "The global water balance",
    label: "Water Cycle · Short video",
    description: "Trace the water exchange between ocean and land through evaporation, precipitation, and runoff. The example also shows why published diagrams need an arithmetic check."
  },
  {
    id: "8csaujmR72U",
    title: "Residence time",
    label: "Water Cycle · Short video",
    description: "Use a water store and its flux to calculate residence time. Compare fast atmospheric turnover with rivers, oceans, and groundwater that can take millennia to renew."
  },
  {
    id: "hBKWLNz9vds",
    title: "Water availability and scarcity",
    label: "Water Cycle · Short video",
    description: "Separate a fixed water store from a renewable annual supply. The video corrects a misleading global water-availability calculation and explains why the distinction matters."
  },
  {
    id: "Aatq0nfuQ8I",
    title: "The water balance equation",
    label: "Water Cycle · Short video",
    description: "Work through rainfall, runoff, evaporation, and storage change in one catchment. The example explains why evaporation can exceed rainfall during a dry period."
  },
  {
    id: "i8lkaLAV2CU",
    title: "Flood probability and recurrence",
    label: "Water Cycle · Short video",
    description: "Understand what a one-in-100-year flood means and what it does not mean. A flood probability applies every year, even immediately after a large event."
  },
  {
    id: "T--Uv3RwnzY",
    title: "Scale and remote sensing",
    label: "Water Cycle · Short video",
    description: "See why point measurements cannot describe the global water cycle on their own. Satellite missions estimate precipitation, evaporation, discharge, and water storage at large scales."
  },
  {
    id: "rbX_gydnvOA",
    title: "Physical properties of water",
    label: "Water Cycle · Extended explainer",
    description: "Explore the molecular structure and unusual properties of water in more detail. The video links polarity, hydrogen bonds, heat storage, and density to Earth’s climate system."
  },
  {
    id: "dSAHvei3GkU",
    title: "Stores, fluxes, and residence time",
    label: "Water Cycle · Extended explainer",
    description: "Build a quantitative view of the global water cycle with stores, fluxes, and residence times. The discussion compares rapid atmospheric change with slow groundwater renewal."
  }
];

window.precipitationVideos = [
  {
    id: "SuStyCqaX58",
    title: "Precipitation and atmospheric moisture",
    label: "Precipitation · Core concept",
    description: "Learn what counts as precipitation and how water vapor behaves in the atmosphere. The video introduces vapor pressure, dew point, and the temperature control on moisture."
  },
  {
    id: "t3ldTbYjXLw",
    title: "How rain begins",
    label: "Precipitation · Core concept",
    description: "Follow the path from water vapor to a falling raindrop. The video explains condensation nuclei, cloud droplets, droplet growth, and the limits of cloud seeding."
  },
  {
    id: "9SJPGTc28qY",
    title: "Ice, hail, and precipitation types",
    label: "Precipitation · Core concept",
    description: "See how ice crystals grow at the expense of supercooled droplets in the Bergeron process. The video also explains hail formation and the main forms of precipitation."
  },
  {
    id: "8-Nsova_1EA",
    title: "Mountains and rain shadows",
    label: "Precipitation · Core concept",
    description: "Learn how topography changes rainfall through uplift, cooling, and descent on the lee side. The video separates an orographic rain shadow from a warm, dry foehn wind."
  },
  {
    id: "CVE_hty9Rsc",
    title: "Dynamic controls on rainfall",
    label: "Precipitation · Core concept",
    description: "Move beyond mountains to examine the atmospheric motion that organizes rainfall. The video links storms, circulation, and changing weather systems to where rain falls."
  },
  {
    id: "8davp81YA7c",
    title: "Why rain gauges disagree",
    label: "Precipitation · Measurement",
    description: "A rain gauge measures a small sample of a storm, not a perfect truth. Learn how wind, wetting, evaporation, and splash create measurement errors."
  },
  {
    id: "OQhosHuCUUY",
    title: "Why snow is hard to measure",
    label: "Precipitation · Measurement",
    description: "See why a rain gauge struggles when precipitation falls as snow. The video compares gauge corrections with measurements of snow depth and water equivalent."
  },
  {
    id: "90t8AucriyE",
    title: "From rain gauges to catchment rainfall",
    label: "Precipitation · Measurement",
    description: "Learn why a few point gauges cannot directly represent rainfall across a catchment. The video introduces spatial averaging, network density, radar, and satellite observations."
  },
  {
    id: "4KGW9nqPzI8",
    title: "Radar rainfall and the Z–R relation",
    label: "Precipitation · Measurement",
    description: "Weather radar measures reflectivity, not rainfall directly. Learn how the Z–R relation converts a radar signal into an estimated rainfall rate and why uncertainty remains."
  },
  {
    id: "f6yPVfKX7nI",
    title: "Why radar rainfall can be wrong",
    label: "Precipitation · Measurement",
    description: "Examine the physical limits of radar rainfall estimates, from beam height to melting layers. The video shows how dual-polarization radar and rain gauges reduce uncertainty."
  }
];

window.waterCountryCommunityVideos = [
  {
    id: "KakMgvx59vU",
    title: "Homily to Country",
    label: "Water, Country and Community · External film",
    description: "Artist JR documents a procession through the dry Menindee Lakes. The work connects ecological decline in the Darling/Baaka with the living cultural heritage of the Baakandji people."
  }
];

window.renderCourseVideos = function (elementId, videos) {
  var container = document.getElementById(elementId);

  if (!container) {
    return;
  }

  container.classList.add("course-video-grid");
  container.replaceChildren();

  videos.forEach(function (video) {
    var article = document.createElement("article");
    var label = document.createElement("p");
    var heading = document.createElement("h3");
    var frame = document.createElement("iframe");
    var description = document.createElement("p");

    article.className = "course-video-card";
    label.className = "course-video-label";
    description.className = "course-video-description";
    label.textContent = video.label;
    heading.textContent = video.title;
    description.textContent = video.description;
    frame.src = "https://www.youtube-nocookie.com/embed/" + video.id;
    frame.title = video.title;
    frame.loading = "lazy";
    frame.allowFullscreen = true;
    frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";

    article.append(label, heading, frame, description);
    container.append(article);
  });
};

document.querySelectorAll("[data-course-videos]").forEach(function (container) {
  var collection = container.dataset.courseVideos;

  if (collection === "water-cycle") {
    window.renderCourseVideos(container.id, window.waterCycleVideos);
  }

  if (collection === "precipitation") {
    window.renderCourseVideos(container.id, window.precipitationVideos);
  }

  if (collection === "water-country-community") {
    window.renderCourseVideos(container.id, window.waterCountryCommunityVideos);
  }
});
