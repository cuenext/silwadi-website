# Lighthouse accessibility raw diagnostics

## tap-targets

```json
undefined
```

## color-contrast

```json
{
  "id": "color-contrast",
  "title": "Background and foreground colors do not have a sufficient contrast ratio.",
  "description": "Low-contrast text is difficult or impossible for many users to read. [Learn how to provide sufficient color contrast](https://dequeuniversity.com/rules/axe/4.12/color-contrast).",
  "score": 0,
  "scoreDisplayMode": "binary",
  "details": {
    "type": "table",
    "headings": [
      {
        "key": "node",
        "valueType": "node",
        "subItemsHeading": {
          "key": "relatedNode",
          "valueType": "node"
        },
        "label": "Failing Elements"
      }
    ],
    "items": [
      {
        "node": {
          "type": "node",
          "lhId": "1-0-P",
          "path": "1,HTML,1,BODY,4,MAIN,0,SECTION,0,DIV,0,DIV,2,P",
          "selector": "section#home > div.container > div.home-hero__copy > p.hero-lead",
          "boundingRect": {
            "top": 295,
            "bottom": 343,
            "left": 15,
            "right": 397,
            "width": 382,
            "height": 48
          },
          "snippet": "<p class=\"hero-lead\">",
          "nodeLabel": "Dental care in Abu Dhabi since 1980, with general dentists and specialists work…",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.31 (foreground color: #637a82, background color: #f7fafb, font size: 10.5pt (14px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-1-SECTION",
                "path": "1,HTML,1,BODY,4,MAIN,0,SECTION",
                "selector": "body > main#main > section#home",
                "boundingRect": {
                  "top": 105,
                  "bottom": 889,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 784
                },
                "snippet": "<section class=\"home-hero\" id=\"home\">",
                "nodeLabel": "DR. MUNIR SILWADI DENTAL CENTRE\n\nAdvanced dentistry.\nEstablished trust.\n\nDental…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-2-SPAN",
          "path": "1,HTML,1,BODY,4,MAIN,0,SECTION,0,DIV,0,DIV,4,DIV,0,SPAN",
          "selector": "div.container > div.home-hero__copy > div.trust-line > span",
          "boundingRect": {
            "top": 438,
            "bottom": 450,
            "left": 15,
            "right": 66,
            "width": 51,
            "height": 12
          },
          "snippet": "<span>",
          "nodeLabel": "Abu Dhabi",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.31 (foreground color: #637a82, background color: #f7fafb, font size: 8.3pt (11px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-1-SECTION",
                "path": "1,HTML,1,BODY,4,MAIN,0,SECTION",
                "selector": "body > main#main > section#home",
                "boundingRect": {
                  "top": 105,
                  "bottom": 889,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 784
                },
                "snippet": "<section class=\"home-hero\" id=\"home\">",
                "nodeLabel": "DR. MUNIR SILWADI DENTAL CENTRE\n\nAdvanced dentistry.\nEstablished trust.\n\nDental…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-3-SPAN",
          "path": "1,HTML,1,BODY,4,MAIN,0,SECTION,0,DIV,1,DIV,2,DIV,1,SPAN",
          "selector": "div.container > div.home-hero__media > div.legacy-seal > span",
          "boundingRect": {
            "top": 543,
            "bottom": 552,
            "left": 328,
            "right": 392,
            "width": 63,
            "height": 9
          },
          "snippet": "<span>",
          "nodeLabel": "ESTABLISHED",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 3.62 (foreground color: #758a91, background color: #ffffff, font size: 6.0pt (8px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-4-DIV",
                "path": "1,HTML,1,BODY,4,MAIN,0,SECTION,0,DIV,1,DIV,2,DIV",
                "selector": "section#home > div.container > div.home-hero__media > div.legacy-seal",
                "boundingRect": {
                  "top": 500,
                  "bottom": 572,
                  "left": 324,
                  "right": 396,
                  "width": 72,
                  "height": 72
                },
                "snippet": "<div class=\"legacy-seal\" aria-label=\"Established since 1980\">",
                "nodeLabel": "1980\nESTABLISHED"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-5-SPAN",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,0,A,0,SPAN",
          "selector": "nav.care-shortcuts > div.container > a > span",
          "boundingRect": {
            "top": 1176,
            "bottom": 1202,
            "left": 30,
            "right": 40,
            "width": 10,
            "height": 26
          },
          "snippet": "<span>",
          "nodeLabel": "01",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 2.37 (foreground color: #9aabb0, background color: #ffffff, font size: 6.8pt (9px), font weight: bold). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-7-EM",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,0,A,2,EM",
          "selector": "nav.care-shortcuts > div.container > a > em",
          "boundingRect": {
            "top": 1192,
            "bottom": 1202,
            "left": 53,
            "right": 191,
            "width": 138,
            "height": 10
          },
          "snippet": "<em>",
          "nodeLabel": "Meet the medical team",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 3.46 (foreground color: #7a8d93, background color: #ffffff, font size: 6.8pt (9px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-8-SPAN",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,1,A,0,SPAN",
          "selector": "nav.care-shortcuts > div.container > a > span",
          "boundingRect": {
            "top": 1176,
            "bottom": 1202,
            "left": 220,
            "right": 230,
            "width": 10,
            "height": 26
          },
          "snippet": "<span>",
          "nodeLabel": "02",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 2.37 (foreground color: #9aabb0, background color: #ffffff, font size: 6.8pt (9px), font weight: bold). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-9-EM",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,1,A,2,EM",
          "selector": "nav.care-shortcuts > div.container > a > em",
          "boundingRect": {
            "top": 1192,
            "bottom": 1202,
            "left": 243,
            "right": 382,
            "width": 139,
            "height": 10
          },
          "snippet": "<em>",
          "nodeLabel": "Find the right care",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 3.46 (foreground color: #7a8d93, background color: #ffffff, font size: 6.8pt (9px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-10-SPAN",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,2,A,0,SPAN",
          "selector": "nav.care-shortcuts > div.container > a > span",
          "boundingRect": {
            "top": 1262,
            "bottom": 1288,
            "left": 30,
            "right": 40,
            "width": 10,
            "height": 26
          },
          "snippet": "<span>",
          "nodeLabel": "03",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 2.37 (foreground color: #9aabb0, background color: #ffffff, font size: 6.8pt (9px), font weight: bold). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-11-EM",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,2,A,2,EM",
          "selector": "nav.care-shortcuts > div.container > a > em",
          "boundingRect": {
            "top": 1278,
            "bottom": 1288,
            "left": 53,
            "right": 191,
            "width": 138,
            "height": 10
          },
          "snippet": "<em>",
          "nodeLabel": "Ask about your plan",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 3.46 (foreground color: #7a8d93, background color: #ffffff, font size: 6.8pt (9px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-12-SPAN",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,3,A,0,SPAN",
          "selector": "nav.care-shortcuts > div.container > a > span",
          "boundingRect": {
            "top": 1262,
            "bottom": 1288,
            "left": 220,
            "right": 230,
            "width": 10,
            "height": 26
          },
          "snippet": "<span>",
          "nodeLabel": "04",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 2.37 (foreground color: #9aabb0, background color: #ffffff, font size: 6.8pt (9px), font weight: bold). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-13-EM",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,3,A,2,EM",
          "selector": "nav.care-shortcuts > div.container > a > em",
          "boundingRect": {
            "top": 1278,
            "bottom": 1288,
            "left": 243,
            "right": 382,
            "width": 139,
            "height": 10
          },
          "snippet": "<em>",
          "nodeLabel": "Visit the centre",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 3.46 (foreground color: #7a8d93, background color: #ffffff, font size: 6.8pt (9px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-14-SPAN",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,4,A,0,SPAN",
          "selector": "nav.care-shortcuts > div.container > a > span",
          "boundingRect": {
            "top": 1348,
            "bottom": 1374,
            "left": 30,
            "right": 40,
            "width": 10,
            "height": 26
          },
          "snippet": "<span>",
          "nodeLabel": "05",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 2.37 (foreground color: #9aabb0, background color: #ffffff, font size: 6.8pt (9px), font weight: bold). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-15-EM",
          "path": "1,HTML,1,BODY,4,MAIN,2,NAV,0,DIV,4,A,2,EM",
          "selector": "nav.care-shortcuts > div.container > a > em",
          "boundingRect": {
            "top": 1364,
            "bottom": 1374,
            "left": 53,
            "right": 382,
            "width": 329,
            "height": 10
          },
          "snippet": "<em>",
          "nodeLabel": "+971 2 626 2042",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 3.46 (foreground color: #7a8d93, background color: #ffffff, font size: 6.8pt (9px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-6-NAV",
                "path": "1,HTML,1,BODY,4,MAIN,2,NAV",
                "selector": "body > main#main > nav.care-shortcuts",
                "boundingRect": {
                  "top": 1146,
                  "bottom": 1405,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 259
                },
                "snippet": "<nav class=\"care-shortcuts\" aria-label=\"Patient shortcuts\">",
                "nodeLabel": "01\nFind a Doctor\nMeet the medical team\n02\nExplore Treatments\nFind the right car…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-16-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,1,DIV,1,A",
          "selector": "footer.site-footer > div.container > div > a",
          "boundingRect": {
            "top": 5845,
            "bottom": 5856,
            "left": 15,
            "right": 190,
            "width": 175,
            "height": 11
          },
          "snippet": "<a href=\"treatments.html\">",
          "nodeLabel": "Treatments",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-18-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,1,DIV,2,A",
          "selector": "footer.site-footer > div.container > div > a",
          "boundingRect": {
            "top": 5865,
            "bottom": 5876,
            "left": 15,
            "right": 190,
            "width": 175,
            "height": 11
          },
          "snippet": "<a href=\"doctors.html\">",
          "nodeLabel": "Doctors",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-19-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,1,DIV,3,A",
          "selector": "footer.site-footer > div.container > div > a",
          "boundingRect": {
            "top": 5885,
            "bottom": 5896,
            "left": 15,
            "right": 190,
            "width": 175,
            "height": 11
          },
          "snippet": "<a href=\"digital-dentistry.html\">",
          "nodeLabel": "Digital Dentistry",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-20-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,2,DIV,1,A",
          "selector": "footer.site-footer > div.container > div > a",
          "boundingRect": {
            "top": 5845,
            "bottom": 5856,
            "left": 222,
            "right": 397,
            "width": 175,
            "height": 11
          },
          "snippet": "<a href=\"about.html\">",
          "nodeLabel": "About",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-21-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,2,DIV,2,A",
          "selector": "footer.site-footer > div.container > div > a",
          "boundingRect": {
            "top": 5865,
            "bottom": 5876,
            "left": 222,
            "right": 397,
            "width": 175,
            "height": 11
          },
          "snippet": "<a href=\"locations.html\">",
          "nodeLabel": "Locations",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-22-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,2,DIV,3,A",
          "selector": "footer.site-footer > div.container > div > a",
          "boundingRect": {
            "top": 5885,
            "bottom": 5896,
            "left": 222,
            "right": 397,
            "width": 175,
            "height": 11
          },
          "snippet": "<a href=\"mailto:info@silwadidentalcentres.ae?subject=Insurance%20Enquiry\">",
          "nodeLabel": "Insurance Enquiry",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-23-SPAN",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,3,DIV,1,ADDRESS,1,SPAN",
          "selector": "div.container > div > address.footer-address > span",
          "boundingRect": {
            "top": 6003,
            "bottom": 6032,
            "left": 15,
            "right": 190,
            "width": 175,
            "height": 29
          },
          "snippet": "<span>",
          "nodeLabel": "Al Hilal Bank, Bani Yas Tower, Building 117 C Floor",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-24-SPAN",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,3,DIV,1,ADDRESS,2,SPAN",
          "selector": "div.container > div > address.footer-address > span",
          "boundingRect": {
            "top": 6037,
            "bottom": 6066,
            "left": 15,
            "right": 190,
            "width": 175,
            "height": 29
          },
          "snippet": "<span>",
          "nodeLabel": "Sultan Bin Zayed The First St, W Corniche Road, Abu Dhabi, UAE",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-25-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,3,DIV,1,ADDRESS,3,A",
          "selector": "div.container > div > address.footer-address > a",
          "boundingRect": {
            "top": 6071,
            "bottom": 6085,
            "left": 15,
            "right": 190,
            "width": 175,
            "height": 15
          },
          "snippet": "<a href=\"tel:+97126262042\">",
          "nodeLabel": "+971 2 626 2042",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-26-A",
          "path": "1,HTML,1,BODY,5,FOOTER,0,DIV,3,DIV,1,ADDRESS,4,A",
          "selector": "div.container > div > address.footer-address > a",
          "boundingRect": {
            "top": 6090,
            "bottom": 6105,
            "left": 15,
            "right": 190,
            "width": 175,
            "height": 15
          },
          "snippet": "<a href=\"mailto:info@silwadidentalcentres.ae\">",
          "nodeLabel": "info@silwadidentalcentres.ae",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 4.03 (foreground color: #687f87, background color: #f8fafb, font size: 7.5pt (10px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-27-SPAN",
          "path": "1,HTML,1,BODY,5,FOOTER,1,DIV,0,SPAN",
          "selector": "body > footer.site-footer > div.container > span",
          "boundingRect": {
            "top": 6166,
            "bottom": 6176,
            "left": 15,
            "right": 397,
            "width": 382,
            "height": 10
          },
          "snippet": "<span>",
          "nodeLabel": "© 2026 Dr. Munir Silwadi Dental Centre",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 2.9 (foreground color: #85979c, background color: #f8fafb, font size: 6.8pt (9px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      },
      {
        "node": {
          "type": "node",
          "lhId": "1-28-SPAN",
          "path": "1,HTML,1,BODY,5,FOOTER,1,DIV,1,SPAN",
          "selector": "body > footer.site-footer > div.container > span",
          "boundingRect": {
            "top": 6183,
            "bottom": 6193,
            "left": 15,
            "right": 397,
            "width": 382,
            "height": 10
          },
          "snippet": "<span>",
          "nodeLabel": "Expert care. Lasting smiles.",
          "explanation": "Fix any of the following:\n  Element has insufficient color contrast of 2.9 (foreground color: #85979c, background color: #f8fafb, font size: 6.8pt (9px), font weight: normal). Expected contrast ratio of 4.5:1"
        },
        "subItems": {
          "type": "subitems",
          "items": [
            {
              "relatedNode": {
                "type": "node",
                "lhId": "1-17-FOOTER",
                "path": "1,HTML,1,BODY,5,FOOTER",
                "selector": "body > footer.site-footer",
                "boundingRect": {
                  "top": 5641,
                  "bottom": 6217,
                  "left": 0,
                  "right": 412,
                  "width": 412,
                  "height": 576
                },
                "snippet": "<footer class=\"site-footer\">",
                "nodeLabel": "Established dental care in Abu Dhabi since 1980.\n\nCARE\nTreatments\nDoctors\nDigit…"
              }
            }
          ]
        }
      }
    ],
    "debugData": {
      "type": "debugdata",
      "impact": "serious",
      "tags": [
        "cat.color",
        "wcag2aa",
        "wcag143",
        "TTv5",
        "TT13.c",
        "EN-301-549",
        "EN-9.1.4.3",
        "ACT",
        "RGAAv4",
        "RGAA-3.2.1"
      ]
    }
  }
}
```

