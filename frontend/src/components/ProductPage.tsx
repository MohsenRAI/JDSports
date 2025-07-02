"use client"

import { useState } from "react"
import { ChevronRight, Star, Plus, Minus, Heart, Truck, RotateCcw, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { TryOnModal } from "@/components/TryOnModal"

export default function ProductPage() {
  const [selectedSize, setSelectedSize] = useState("M")
  const [quantity, setQuantity] = useState(0)
  const [selectedImage, setSelectedImage] = useState(0)
  const [isTryOnModalOpen, setIsTryOnModalOpen] = useState(false)

  const productImages = [
    "https://images.asos-media.com/products/jordan-brooklyn-fleece-hoodie-in-red/206084313-4?$n_640w$&wid=513&fit=constrain", // Main red hoodie
    "https://images.asos-media.com/products/jordan-brooklyn-fleece-sweatshirt-in-red/204900049-1-red?$n_640w$&wid=513&fit=constrain", // Red sweatshirt
    "https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/824eb89b-b893-4bb2-9df6-63941d6392b5/MJ+BROOKLYN+FLC+PO.png", // Kids red hoodie
    "https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/ebf3bde4-2568-43ce-a975-e255ddb5ab7c/M+J+BRK+OVS+GFX+FZ+HD.png", // Black zip hoodie
    "https://www.shoepalace.com/cdn/shop/products/24509a053de2ca40b987c60076936d77_2048x2048.jpg?v=1707870838", // All-over print
  ]

  const sizes = ["S", "M", "L", "XL", "XXL"]
  const colors = [
    { name: "Black", color: "bg-black", selected: false },
    { name: "Red", color: "bg-red-600", selected: true },
  ]

  return (
    <div className="bg-white">
      {/* Breadcrumb */}
      <div className="px-4 py-3 text-sm text-gray-600">
        <div className="flex items-center gap-2">
          <span className="hover:text-black cursor-pointer">JD Sports</span>
          <ChevronRight className="h-3 w-3" />
          <span className="hover:text-black cursor-pointer">Men's</span>
          <ChevronRight className="h-3 w-3" />
          <span className="hover:text-black cursor-pointer">Clothing</span>
          <ChevronRight className="h-3 w-3" />
          <span>Hoodies</span>
        </div>
      </div>

      {/* Product Section */}
      <div className="px-4 py-8">
        <div className="flex gap-8">
          {/* Product Images */}
          <div className="flex gap-4">
            {/* Thumbnails */}
            <div className="flex flex-col gap-3">
              {productImages.slice(1).map((image, index) => (
                <div
                  key={`thumbnail-${index}`}
                  className={`w-20 h-24 border-2 cursor-pointer rounded-lg overflow-hidden ${
                    selectedImage === index + 1 ? "border-black" : "border-gray-200"
                  }`}
                  onClick={() => setSelectedImage(index + 1)}
                >
                  <img
                    src={image}
                    alt={`Product ${index + 1}`}
                    className="w-full h-full object-cover"
                  />
                </div>
              ))}
            </div>

            {/* Main Image */}
            <div className="relative">
              <img
                src={productImages[0]}
                alt="Jordan Hoodie"
                className="w-96 h-auto object-cover bg-gray-100 rounded-lg"
              />
              <div className="absolute top-4 left-4">
                <div className="text-black font-bold text-xl">JORDAN</div>
              </div>
              <div className="absolute top-4 right-4 bg-white rounded-full p-2 cursor-pointer shadow-md">
                🔍
              </div>
            </div>
          </div>

          {/* Product Details */}
          <div className="flex-1 max-w-md">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              JORDAN MEN'S BROOKLYN FLEECE PULLOVER HOODIE
            </h1>

            <div className="flex items-center gap-3 mb-4">
              <span className="text-2xl font-bold">$54.99</span>
              <Badge variant="outline" className="text-xs">
                +4 JD Cash
              </Badge>
            </div>

            {/* Rating */}
            <div className="flex items-center gap-2 mb-6">
              <div className="flex items-center">
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star
                    key={star}
                    className={`h-4 w-4 ${
                      star <= 4 ? "fill-black text-black" : "text-gray-300"
                    }`}
                  />
                ))}
              </div>
              <span className="text-sm font-medium">4.9</span>
              <span className="text-sm text-gray-600">(26)</span>
            </div>

            {/* Available Colors */}
            <div className="mb-6">
              <h3 className="text-sm font-medium mb-3">Available colors</h3>
              <div className="flex gap-2">
                {colors.map((color, index) => (
                  <div
                    key={`color-${color.name}`}
                    className={`w-12 h-12 rounded-lg border-2 cursor-pointer relative overflow-hidden ${
                      color.selected ? "border-black" : "border-gray-200"
                    }`}
                  >
                    <div className={`w-full h-full ${color.color}`} />
                  </div>
                ))}
              </div>
            </div>

            {/* Size Selection */}
            <div className="mb-6">
              <h3 className="text-sm font-medium mb-3">Select size</h3>
              <div className="flex gap-2 mb-3">
                {sizes.map((size) => (
                  <button
                    key={size}
                    onClick={() => setSelectedSize(size)}
                    className={`px-4 py-2 border rounded-lg text-sm font-medium ${
                      selectedSize === size
                        ? "border-black bg-black text-white"
                        : "border-gray-300 bg-white text-gray-900 hover:border-gray-400"
                    }`}
                  >
                    {size}
                  </button>
                ))}
              </div>
              <button className="text-sm text-gray-600 underline flex items-center gap-1">
                📏 Size guide
              </button>
            </div>

            {/* Quantity and Add to Cart */}
            <div className="mb-6">
              <h3 className="text-sm font-medium mb-3">Quantity</h3>
              <div className="flex items-center gap-4 mb-4">
                <div className="flex items-center border border-gray-300 rounded-lg">
                  <button
                    onClick={() => setQuantity(Math.max(0, quantity - 1))}
                    className="p-2 hover:bg-gray-50"
                  >
                    <Minus className="h-4 w-4" />
                  </button>
                  <span className="px-4 py-2 min-w-[3rem] text-center">{quantity}</span>
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="p-2 hover:bg-gray-50"
                  >
                    <Plus className="h-4 w-4" />
                  </button>
                </div>
                <Button className="flex-1 bg-teal-500 hover:bg-teal-600 text-white font-medium py-3">
                  Add to basket
                </Button>
                <button className="p-3 border border-gray-300 rounded-lg hover:bg-gray-50">
                  <Heart className="h-5 w-5" />
                </button>
              </div>

              {/* Try on with AI Button */}
              <Button 
                onClick={() => setIsTryOnModalOpen(true)}
                className="w-full bg-teal-500 hover:bg-teal-600 text-white font-medium py-3 mt-3"
              >
                🤖 Try on with AI
              </Button>
            </div>

            {/* Store Availability */}
            <div className="mb-6">
              <button className="text-sm text-gray-700 underline">
                Check availability in store →
              </button>
            </div>

            {/* Delivery Info */}
            <div className="space-y-3 text-sm">
              <div className="flex items-center gap-3">
                <Truck className="h-4 w-4 text-gray-600" />
                <span>Free delivery from $50</span>
              </div>
              <div className="flex items-center gap-3">
                <RotateCcw className="h-4 w-4 text-gray-600" />
                <span>30 days free returns</span>
              </div>
              <div className="flex items-center gap-3">
                <Clock className="h-4 w-4 text-gray-600" />
                <span>Standard delivery: 2 - 4 working days</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Try On Modal */}
      <TryOnModal
        isOpen={isTryOnModalOpen}
        onClose={() => setIsTryOnModalOpen(false)}
        selectedColor="red"
      />
    </div>
  )
}
