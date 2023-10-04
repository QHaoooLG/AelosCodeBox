Blockly.Blocks['1632297617946'] = {
  init: function() {
    this.jsonInit({
      "type": "1632297617946",
      "message0": "boxturn009R",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632297617946'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(30,30,30,85,85,85,85,85,30,30,30,85,85,85,85,85,0,0,0)\nMOTOsetspeed(50)\nMOTOmove19(100, 185, 100, 102, 93, 55, 124, 98, 100, 15, 100, 98, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(30,30,30,85,85,85,85,75,30,30,30,85,85,85,85,45,0,0,0)\nMOTOsetspeed(100)\nMOTOmove19(100, 185, 100, 97, 87, 55, 121, 90, 100, 15, 100, 97, 101, 145, 79, 97, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 100, 90, 85, 55, 120, 90, 100, 15, 100, 95, 104, 146, 76, 92, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(30,30,30,30,30,30,30,30,30,30,30,65,75,80,75,65,0,0,0)\n\n\n-- MOTORB,105,62,168,83,95\nMOTOsetspeed(25)\nMOTOmove19(100, 185, 100, 93, 103, 73, 115, 88, 100, 15, 100, 95, 104, 146, 76, 92, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(25)\nMOTOmove19(100, 185, 100, 100, 93, 55, 124, 98, 100, 15, 100, 100, 107, 145, 76, 102, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

