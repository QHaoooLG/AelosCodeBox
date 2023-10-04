Blockly.Blocks['1632296815232'] = {
  init: function () {
    this.jsonInit({
      "type": "1632296815232",
      "message0": "boxDown3",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632296815232'] = function (block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(60,60,60,30,60,60,60,30,60,60,60,30,60,60,60,30,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(100, 185, 100, 98, 93, 55, 124, 98, 100, 15, 100, 102, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 100, 98, 93, 55, 124, 98, 100, 15, 100, 102, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(100,100,100,100,80,80,80,30,100,100,100,100,80,80,80,30,0,0,0)\nMOTOsetspeed(14)\nMOTOmove19(100, 185, 15, 98, 93, 55, 124, 98, 100, 15, 185, 102, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(14)\nMOTOmove19(110, 155, 15, 98, 93, 55, 124, 98, 90, 45, 185, 102, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\nDelayMs(500)\nMOTOrigid16(100,100,100,100,80,80,80,30,100,100,100,100,80,80,80,30,0,0,0)\nMOTOsetspeed(30)\nMOTOmove19(80, 165, 100, 98, 93, 55, 124, 98, 120, 35, 100, 102, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(30)\nMOTOmove19(80, 30, 100, 100, 93, 55, 124, 100, 120, 170, 100, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

Blockly.Blocks['Right_flank_kick'] = {
  init: function () {
    this.jsonInit({
      type: "Right_flank_kick",
      message0: "%{BKY_RIGHT_FLANK_KICK}",
      previousStatement: null,
      nextStatement: null,
      colour: "#7148F5",
      toolip: "",
      helpUrl: ""
    });
  }
};

Blockly.Lua['Right_flank_kick'] = function (block) {
  const code = [
    "MOTOrigid16(25,25,25,70,70,70,70,70,25,25,25,70,70,70,70,70)",
    "MOTOsetspeed(15)",
    "MOTOmove16(80, 30, 100, 103, 93, 55, 124, 103, 120, 170, 100, 103, 107, 145, 76, 103)",
    "MOTOwait()",
    "MOTOmove16(80, 40, 100, 105, 93, 54, 124, 105, 120, 160, 100, 110, 109, 152, 71, 112)",
    "MOTOwait()",
    "MOTOmove16(80, 40, 100, 105, 93, 54, 124, 110, 120, 160, 100, 110, 109, 152, 71, 112)",
    "MOTOwait()",
    "MOTOsetspeed(65)",
    "MOTOmove16(80, 60, 100, 105, 93, 55, 124, 114, 120, 140, 100, 140, 95, 115, 95, 120)",
    "MOTOwait()",
    "DelayMs(50)",
    "MOTOsetspeed(36)",
    "MOTOmove16(80, 35, 100, 104, 93, 54, 124, 100, 120, 165, 100, 110, 109, 152, 71, 112)",
    "MOTOwait()",
    "MOTOsetspeed(12)",
    "MOTOmove16(80, 30, 100, 100, 93, 55, 124, 98, 120, 170, 100, 100, 107, 145, 76, 102)",
    "MOTOwait()",
    ""
  ];
  return code.join("\n");
}

Blockly.Blocks['Front_Roll'] = {
  init: function () {
    this.jsonInit({
      type: "Front_Roll",
      message0: "%{BKY_FRONT_ROLL}",
      previousStatement: null,
      nextStatement: null,
      colour: "#48BCBC",
      toolip: "",
      helpUrl: ""
    });
  }
};

Blockly.Lua['Front_Roll'] = function (block) {
  const code = [
    "MOTOrigid16(60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60)",
    "MOTOsetspeed(30)",
    "MOTOmove16(80, 30, 100, 98, 97, 145, 41, 99, 120, 170, 100, 100, 98, 53, 159, 99)",
    "MOTOwait()",
    "MOTOsetspeed(32)",
    "MOTOmove16(85, 30, 130, 100, 140, 177, 45, 100, 115, 170, 70, 100, 60, 23, 155, 100)",
    "MOTOwait()",
    "MOTOsetspeed(35)",
    "MOTOmove16(100, 10, 185, 100, 165, 145, 35, 100, 100, 190, 15, 100, 35, 55, 165, 100)",
    "MOTOwait()",
    "MOTOsetspeed(30)",
    "MOTOmove16(75, 89, 190, 100, 140, 90, 40, 100, 129, 108, 10, 100, 60, 110, 160, 100)",
    "MOTOwait()",
    "MOTOsetspeed(40)",
    "MOTOmove16(57, 79, 131, 100, 140, 90, 40, 100, 138, 131, 66, 100, 60, 110, 160, 100)",
    "MOTOwait()",
    "MOTOsetspeed(80)",
    "MOTOmove16(44, 69, 190, 100, 26, 100, 146, 100, 162, 134, 10, 100, 174, 105, 52, 100)",
    "MOTOwait()",
    "DelayMs(100)",
    "MOTOsetspeed(68)",
    "MOTOmove16(47, 56, 190, 100, 26, 100, 146, 100, 160, 131, 10, 100, 174, 105, 52, 100)",
    "MOTOwait()",
    "DelayMs(100)",
    "MOTOsetspeed(37)",
    "MOTOmove16(115, 176, 127, 101, 51, 174, 33, 101, 85, 24, 78, 99, 153, 28, 165, 102)",
    "MOTOwait()",
    "MOTOsetspeed(37)",
    "MOTOmove16(116, 177, 160, 101, 51, 174, 33, 101, 84, 24, 43, 99, 153, 28, 165, 102)",
    "MOTOwait()",
    "MOTOsetspeed(37)",
    "MOTOmove16(116, 177, 160, 101, 51, 150, 33, 101, 84, 24, 43, 99, 153, 50, 165, 102)",
    "MOTOwait()",
    "MOTOsetspeed(40)",
    "MOTOmove16(116, 177, 160, 100, 69, 139, 43, 100, 86, 24, 43, 99, 134, 61, 162, 101)",
    "MOTOwait()",
    "MOTOsetspeed(40)",
    "MOTOmove16(97, 25, 170, 100, 102, 149, 61, 100, 122, 164, 29, 100, 104, 50, 148, 99)",
    "MOTOwait()",
    "MOTOsetspeed(37)",
    "MOTOmove16(69, 64, 100, 101, 100, 174, 33, 101, 121, 130, 99, 99, 100, 28, 165, 102)",
    "MOTOwait()",
    "DelayMs(100)",
    "MOTOsetspeed(20)",
    "MOTOmove16(83, 28, 98, 100, 123, 152, 44, 103, 115, 169, 89, 103, 78, 46, 161, 100)",
    "MOTOwait()",
    "DelayMs(100)",
    "MOTOsetspeed(15)",
    "MOTOmove16(85, 30, 102, 99, 107, 150, 44, 100, 115, 162, 96, 99, 94, 50, 159, 98)",
    "MOTOwait()",
    "MOTOsetspeed(15)",
    "MOTOmove16(85, 30, 102, 102, 110, 73, 116, 101, 115, 162, 96, 106, 91, 122, 84, 99)",
    "MOTOwait()",
    ""
  ];
  return code.join("\n");
}

