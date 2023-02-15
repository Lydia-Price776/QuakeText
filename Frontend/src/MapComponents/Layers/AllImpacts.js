import LayerGroup from "ol/layer/Group";
import DamageLayer from "./ImpactLayers/DamageLayer";
import DeathLayer from "./ImpactLayers/DeathLayer";
import FireLayer from "./ImpactLayers/FireLayer";
import FloodLayer from "./ImpactLayers/FloodLayer";
import InjuryLayer from "./ImpactLayers/InjuryLayer";
import MissingLayer from "./ImpactLayers/MissingLayer";
import OtherLayer from "./ImpactLayers/OtherLayer";
import TerrorismLayer from "./ImpactLayers/TerrorismLayer";
import TrappedLayer from "./ImpactLayers/TrappedLayer";

const impactLayers = new LayerGroup({
    layers: [
        DamageLayer,  DeathLayer, FireLayer,
        FloodLayer, InjuryLayer, MissingLayer,
        TerrorismLayer, TrappedLayer, OtherLayer
    ]
});

export default impactLayers;