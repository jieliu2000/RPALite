| *** Settings *** |
| Library | RPALite
| Library | BeyondRPA.Edge

| *** Test Cases *** |
|  xdirect script for turning off "Total & average" toggle in Content analytics page
# Open Edge browser
|	| Open Edge Browser |

# Navigate to test URL
|	| Open Web Link | https://int1.msn.com/en-us/partnerhub/home |

# Verify test page loads successfully
|	| Validate Text On Screen | home |

# Click on Content Analytics button
|	| Mouse Click By Text | Content analytics |

# Scroll to the necessary area
|	| Scroll To Page Bottom |

# Verify Toggle display
|	| Validate Text In Window | Overview | Total 0 item(s) |

# Check Toggle is ON
|	| Validate Switch Icon Status | Total & average |

# Turn off Toggle
|	| Click Icon | Total & average |

# Verify Toggle is OFF
|	| Validate Switch Icon Status | Total & average |
