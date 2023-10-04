Blockly.Blocks['1632296803763'] = {
  init: function() {
    this.jsonInit({
      "type": "1632296803763",
      "message0": "boxBack0.5",
      "previousStatement": null,
      "nextStatement": null,
      "colour": '#C643F1',
      "toolip": "",
      "helpUrl": ""
    });
  }
};

Blockly.Lua['1632296803763'] = function(block) {
  var code = "MOTOsetspeed(30)\nMOTOrigid16(100,100,100,65,100,100,100,65,100,100,100,65,100,100,100,65,0,0,0)\nMOTOsetspeed(45)\nMOTOmove19(100, 185, 101, 100, 93, 55, 124, 100, 100, 15, 99, 100, 107, 145, 76, 100, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(100,100,100,85,50,50,50,85,100,100,100,85,50,50,50,85,0,0,0)\nMOTOrigid16(100,100,100,85,60,60,60,75,100,100,100,85,60,60,60,75,0,0,0)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 105, 93, 55, 124, 108, 100, 15, 99, 111, 102, 136, 78, 112, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 101, 105, 93, 55, 124, 107, 100, 15, 99, 108, 125, 145, 94, 105, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(15)\nMOTOmove19(100, 185, 101, 92, 116, 55, 144, 85, 100, 15, 99, 95, 107, 145, 76, 93, 128, 71, 100)\nMOTOwait()\nDelayMs(100)\nMOTOsetspeed(15)\nMOTOmove19(100, 185, 101, 89, 93, 64, 122, 88, 100, 15, 99, 95, 108, 145, 76, 93, 128, 71, 100)\nMOTOwait()\nMOTOrigid16(100,100,100,30,60,60,60,30,100,100,100,30,60,60,60,30,0,0,0)\nMOTOsetspeed(6)\nMOTOmove19(100, 185, 101, 100, 94, 55, 123, 98, 100, 15, 99, 100, 106, 145, 77, 102, 128, 71, 100)\nMOTOwait()\nMOTOsetspeed(20)\nMOTOmove19(100, 185, 100, 100, 94, 55, 124, 100, 100, 15, 100, 100, 106, 145, 76, 100, 128, 71, 100)\nMOTOwait()\n";
  return code;
}

