# YouTube Hashtag Shorts Scraper

> This tool collects structured data from YouTube Shorts based on any hashtag you provide. It helps you uncover trending videos, monitor niches, and gather performance insights without limits. The scraper focuses on delivering clean, reliable data for research, analysis, and automation.

> Built for creators, analysts, and marketers who need accurate YouTube Shorts information fast.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>YouTube Hashtag Shorts Scraper #️⃣📺 - Fast & cheap</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project retrieves detailed information from YouTube Shorts matched to a specific hashtag. It removes the need for manual browsing or platform restrictions, giving you direct access to titles, URLs, thumbnails, and view counts. Anyone working with short-form video analysis, content strategy, or market research will find it especially useful.

### Why Hashtag-Based Scraping Matters

- Lets you target precise niches or communities.
- Reveals real-time trending content in any category.
- Supports competitive research across creators and brands.
- Speeds up data gathering for campaigns or reports.
- Helps automate content discovery workflows.

## Features

| Feature | Description |
|---------|-------------|
| Hashtag-driven extraction | Pulls Shorts data using any keyword or tag you choose. |
| High-volume scraping | Designed to collect large sets of Shorts without limits. |
| Clean metadata output | Provides structured fields for easy analysis and automation. |
| Multi-format export | Enables downloading results in JSON, CSV, XML, and more. |
| Efficient navigation engine | Moves through Shorts reliably to maximize data coverage. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|------------|------------------|
| ID | Incremental identifier for each collected record. |
| Title | Full title text of the YouTube Short. |
| View Count | Text-based view count such as “7M views.” |
| Short URL | Direct link to the Short. |
| Thumbnail URL | High-quality thumbnail image URL. |
| Short ID | Unique YouTube identifier for the Short. |

---

## Example Output


    [
        {
            "ID": 1,
            "Title": "Eyes Lance // Amazing Eyes Transition",
            "View Count": "7M views",
            "Short URL": "https://www.youtube.com/shorts/7wTcL380EwU",
            "Thumbnail URL": "https://i.ytimg.com/vi/7wTcL380EwU/oardefault.jpg",
            "Short ID": "7wTcL380EwU"
        },
        {
            "ID": 2,
            "Title": "Unique Face Mask Made in China",
            "View Count": "4.4M views",
            "Short URL": "https://www.youtube.com/shorts/mt0hPr_BMdk",
            "Thumbnail URL": "https://i.ytimg.com/vi/mt0hPr_BMdk/oardefault.jpg",
            "Short ID": "mt0hPr_BMdk"
        }
    ]

---

## Directory Structure Tree


    YouTube Hashtag Shorts Scraper #️⃣📺 - Fast & cheap/
    ├── src/
    │   ├── runner.py
    │   ├── extractors/
    │   │   ├── youtube_parser.py
    │   │   └── utils_format.py
    │   ├── outputs/
    │   │   └── exporters.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── inputs.sample.json
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- Analysts use it to track niche-specific Shorts content, so they can report on trends quickly.
- Marketers use it to monitor campaign-related hashtags, so they can measure audience engagement.
- Creators use it to study competing Shorts, so they can refine their content strategy.
- Agencies use it to automate research for clients, saving time on manual video discovery.
- Researchers use it to build datasets for studying short-form content behavior.

---

## FAQs

**Does it require login or authentication?**
No, the scraper collects publicly available Shorts data without requiring user authentication.

**How many Shorts can I extract at once?**
You can specify any amount through the `max_items` parameter, and the scraper will continue until the limit is reached or results are exhausted.

**Can I target multiple hashtags at the same time?**
The tool processes one hashtag per run. You can queue or batch runs if you need multiple tags collected.

**Is the data export compatible with analytics tools?**
Yes. JSON, CSV, and XML outputs integrate easily with BI dashboards, notebooks, or automation engines.

---

## Performance Benchmarks and Results

**Primary Metric:** Handles several hundred Shorts per minute on average, depending on hashtag density and connection speed.
**Reliability Metric:** Maintains a high completion rate with minimal dropped records.
**Efficiency Metric:** Optimizes navigation to avoid redundant page loads, resulting in low resource usage.
**Quality Metric:** Produces consistent, well-structured fields with high data completeness across collected Shorts.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
