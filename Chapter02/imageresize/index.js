/**
 * Triggered from a message on a Cloud Storage bucket.
 *
 * @param {!Object} event The Cloud Functions event.
 * @param {!Function} The callback function.
 */
// Code modified from https://github.com/firebase/functions-samples/blob/master/image-sharp/functions/index.js
/**
 * Copyright 2016 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'use strict';

const storage = require('@google-cloud/storage')();
const path = require('path');
const sharp = require('sharp');
const async = require('async');
const config = require('./config.json');

/**
 * When an image is uploaded in the Storage bucket We generate a thumbnail automatically using
 * Sharp.
 */
exports.imageresize = function(event, callback){
  const object = event.data; // The Storage object.

  const fileBucket = object.bucket; // The Storage bucket that contains the file.
  const filePath = object.name; // File path in the bucket.
  const contentType = object.contentType; // File content type.
  const resourceState = object.resourceState; // The resourceState is 'exists' or 'not_exists' (for file/folder deletions).
  const metageneration = object.metageneration; // Number of times metadata has been generated. New objects have a value of 1.

  // Exit if this is triggered on a file that is not an image.
  if (!contentType.startsWith('image/')) {
    console.log('This is not an image.');
    callback();
	return;
  }

  // Get the file name.
  const fileName = path.basename(filePath);
  // Exit if the image is already a thumbnail.
  if (fileName.startsWith('CR_')) {
    console.log('Already resized file.');
    callback();
	return;
  }

  // Exit if this is a move or deletion event.
  if (resourceState === 'not_exists') {
    console.log('This is a deletion event.');
    callback();
	return;
  }

  // Exit if file exists but is not new and is only being triggered
  // because of a metadata change.
  if (resourceState === 'exists' && metageneration > 1) {
    console.log('This is a metadata change event.');
    callback();
	return;
  }

  // Download file from bucket.
  const bucket = storage.bucket(fileBucket);

  const metadata = {
    contentType: contentType
  };
  var itemsResized = 0;
  var config_size = Object.keys(config).length;
  console.log("config size" + config_size);
  //for (var size in config) {
  async.forEachOf(config, function (size, key, cb) {    
 	const MIN = size["min"];
	const MAX = size["max"];
        const size_name = size["name"];
	console.log(size_name + " " + MIN + " " + size["max"]);

	  // We add a 'thumb_' prefix to thumbnails file name. That's where we'll upload the thumbnail.
	  const tempFileName = `CR_${size_name}_${fileName}`;
	  const tempFilePath = path.join(path.dirname(filePath),size_name, tempFileName);
	  // Create write stream for uploading thumbnail
	  const tempFileUploadStream = bucket.file(tempFilePath).createWriteStream({metadata});

	  // Create Sharp pipeline for resizing the image and use pipe to read from bucket read stream
	  const pipeline = sharp();
	  pipeline
		.resize(MIN, MAX)
		.max()
		.pipe(tempFileUploadStream);

	  bucket.file(filePath).createReadStream().pipe(pipeline);
	  
	  tempFileUploadStream.on('error', () => {
			console.log('Resize file creation failed in UploadStream');
			return cb("Resize failed");
			})
		.on('finish',() => {
			console.log('Resize file created successfully');
			cb();
			});
  },
  function (err) { // After iterating through all the elements of the config object
    if (err) console.error(err.message);
    console.log("Done");
    callback();
    return;
  });
};
