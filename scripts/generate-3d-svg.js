import fs from 'fs';
import { Scene, PerspectiveCamera, Mesh, BoxGeometry, MeshBasicMaterial } from 'three';
import { SVGRenderer } from 'three/examples/jsm/renderers/SVGRenderer.js';

const width = 600;
const height = 400;
const renderer = new SVGRenderer();
renderer.setSize(width, height);

const scene = new Scene();
const camera = new PerspectiveCamera(75, width / height, 0.1, 1000);
camera.position.z = 3;

const geometry = new BoxGeometry();
const material = new MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
const cube = new Mesh(geometry, material);
scene.add(cube);

// Rotate the cube for a dynamic angle
cube.rotation.x = Math.PI / 4;
cube.rotation.y = Math.PI / 4;

renderer.render(scene, camera);
const svgData = renderer.domElement.outerHTML;
fs.writeFileSync('assets/3d-scene.svg', svgData);
