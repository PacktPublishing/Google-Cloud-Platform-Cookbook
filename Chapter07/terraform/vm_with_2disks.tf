// Configure the Google Cloud provider
provider "google" {
  //credentials = "${var.GOOGLE_APPLICATION_CREDENTIALS}"
  project     = "upbeat-aura-163616"
  region      = "us-central1"
}

variable "diskType" {
  description = "Disk types"
  type = "list"
  default = ["pd-standard", "pd-ssd"]
}

variable "diskName" {
  description = "Disk names"
  type = "list"
  default = ["backup", "cache"]
}

resource "google_compute_disk" "AddlnDisks" {
  count = 2
  name  = "${element(var.diskName, count.index)}"
  type  = "${element(var.diskType, count.index)}"
  zone  = "us-central1-a"
  size = 10
  labels {
    environment = "dev"
  }
}

resource "google_compute_instance" "instance1" {
  name         = "vm-with-disks"
  machine_type = "f1-micro"
  zone         = "us-central1-a"

  tags = ["foo", "bar"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-8"
    }
  }

  attached_disk {
        source      = "${element(google_compute_disk.AddlnDisks.*.self_link, 1)}"
        device_name = "${element(google_compute_disk.AddlnDisks.*.name, 1)}"
   }
  attached_disk {
        source      = "${element(google_compute_disk.AddlnDisks.*.self_link, 2)}"
        device_name = "${element(google_compute_disk.AddlnDisks.*.name, 2)}"
   }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }

  metadata {
    foo = "bar"
  }

  metadata_startup_script = "echo hi > /test.txt"

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }

  //depends_on = ["google_compute_disk.default"]
}

output "instance_id" {
  value = "${google_compute_instance.instance1.self_link}"
}

